# Phase 01: Code Fix — DB-Level Filtering & SearchMatchingService Slim

**Status:** Ready
**Priority:** High

## Context Links

- `backend/Hmss.Api/Repositories/Interfaces/IRoomListingRepository.cs`
- `backend/Hmss.Api/Repositories/Implementations/RoomListingRepository.cs`
- `backend/Hmss.Api/Services/SearchMatchingService.cs`
- `backend/Hmss.Api/Controllers/RoomSearchController.cs`
- `backend/Hmss.Api/DTOs/Search/SearchCriteriaDto.cs`

## Overview

Move criteria filtering from `SearchMatchingService` (in-memory LINQ) into `IRoomListingRepository.FindByCriteriaAsync` (DB-level EF Core query). This matches the design spec message `2.2: Controller → IRoomListingRepository: FindByCriteriaAsync(...)` and removes the unnecessary full-table load.

`SearchMatchingService.FilterByCriteria` is deleted. `BuildListingSummaries` stays.

## Key Insight — Amenities Filter

`Amenities` is stored as a JSON string (`"[\"WiFi\",\"AC\"]"`). EF Core cannot translate JSON array logic to SQL. Solution: apply all filterable fields at DB level in EF Core, then filter amenities **in-memory inside the repository method** after `ToListAsync()`. This keeps the controller clean while still moving the majority of filtering to DB.

## SearchCriteriaDto Fields

```csharp
public string? Location { get; set; }       // LIKE on Property.Address or Title
public decimal? MinPrice { get; set; }       // DB: x.Price >= value
public decimal? MaxPrice { get; set; }       // DB: x.Price <= value
public List<string>? Amenities { get; set; } // In-memory (JSON string field)
public DateOnly? AvailableFrom { get; set; } // DB: x.AvailableFrom <= value
public string? FurnishedStatus { get; set; } // DB: equality
public bool? PrivateWC { get; set; }         // DB: x.PrivateWCStatus == "Private"
```

## Implementation Steps

### Step 1 — IRoomListingRepository.cs: Add method signature

```csharp
Task<List<RoomListing>> FindByCriteriaAsync(SearchCriteriaDto criteria);
```

Add `using Hmss.Api.DTOs.Search;` at top if not present.

### Step 2 — RoomListingRepository.cs: Implement FindByCriteriaAsync

```csharp
public async Task<List<RoomListing>> FindByCriteriaAsync(SearchCriteriaDto criteria)
{
    var query = _db.RoomListings
        .Include(x => x.Property)
        .Where(x => x.Status == "PublishedAvailable")
        .AsQueryable();

    if (!string.IsNullOrWhiteSpace(criteria.Location))
    {
        var loc = criteria.Location.ToLower();
        query = query.Where(x =>
            (x.Property != null && x.Property.Address.ToLower().Contains(loc)) ||
            x.Title.ToLower().Contains(loc));
    }

    if (criteria.MinPrice.HasValue)
        query = query.Where(x => x.Price >= criteria.MinPrice.Value);

    if (criteria.MaxPrice.HasValue)
        query = query.Where(x => x.Price <= criteria.MaxPrice.Value);

    if (criteria.AvailableFrom.HasValue)
        query = query.Where(x => x.AvailableFrom <= criteria.AvailableFrom.Value);

    if (!string.IsNullOrWhiteSpace(criteria.FurnishedStatus))
        query = query.Where(x => x.FurnishedStatus == criteria.FurnishedStatus);

    if (criteria.PrivateWC.HasValue && criteria.PrivateWC.Value)
        query = query.Where(x => x.PrivateWCStatus == "Private");

    var listings = await query.ToListAsync();

    // Amenities stored as JSON string — must filter in-memory after DB fetch
    if (criteria.Amenities != null && criteria.Amenities.Count > 0)
    {
        listings = listings.Where(x =>
        {
            if (string.IsNullOrWhiteSpace(x.Amenities)) return false;
            try
            {
                var amenities = JsonSerializer.Deserialize<List<string>>(x.Amenities) ?? new();
                return criteria.Amenities.All(a =>
                    amenities.Contains(a, StringComparer.OrdinalIgnoreCase));
            }
            catch { return false; }
        }).ToList();
    }

    return listings;
}
```

Add `using System.Text.Json;` at top.

### Step 3 — SearchMatchingService.cs: Replace FilterByCriteria with ValidateCriteria

Delete `FilterByCriteria`. Add `ValidateCriteria`. Keep `BuildListingSummaries` (implicit DTO mapping, not shown in diagram).

```csharp
/// <summary>
/// Validates search criteria before querying the repository.
/// Empty/null criteria is valid — means "return all published listings".
/// </summary>
public (bool IsValid, string? Error) ValidateCriteria(SearchCriteriaDto criteria)
{
    if (criteria.MinPrice.HasValue && criteria.MaxPrice.HasValue
        && criteria.MinPrice.Value > criteria.MaxPrice.Value)
        return (false, "MinPrice cannot be greater than MaxPrice.");

    return (true, null);
}
```

### Step 4 — RoomSearchController.cs: Update SearchRooms

Replace:
```csharp
var allListings = await _listingRepo.FindPublishedListingsAsync();
var filtered = _searchService.FilterByCriteria(allListings, criteria);
var summaries = _searchService.BuildListingSummaries(filtered);
```

With:
```csharp
var (isValid, error) = _searchService.ValidateCriteria(criteria);
if (!isValid) return BadRequest(error);

var filtered = await _listingRepo.FindByCriteriaAsync(criteria);
var summaries = _searchService.BuildListingSummaries(filtered);
```

`GetSearchPage` (sequence 1) is unchanged — still calls `FindPublishedListingsAsync` + `BuildListingSummaries`.

## Todo

- [ ] Add `FindByCriteriaAsync` signature to `IRoomListingRepository.cs`
- [ ] Implement `FindByCriteriaAsync` in `RoomListingRepository.cs`
- [ ] Replace `FilterByCriteria` with `ValidateCriteria` in `SearchMatchingService.cs`
- [ ] Update `RoomSearchController.SearchRooms`: call `ValidateCriteria` then `FindByCriteriaAsync`
- [ ] Run `dotnet build` — verify zero errors

## Success Criteria

- `dotnet build` passes with zero errors
- `IRoomListingRepository` has `FindByCriteriaAsync(SearchCriteriaDto)`
- `SearchMatchingService` has `ValidateCriteria` + `BuildListingSummaries` (no `FilterByCriteria`)
- `RoomSearchController.SearchRooms` validates first, then calls repo directly
