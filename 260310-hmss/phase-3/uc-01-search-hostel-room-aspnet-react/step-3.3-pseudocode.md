# UC-01 Search Hostel Room - C# Design Skeleton

## Notes

- This is C#-style design code derived from:
  - `step-3.0-design-communication-diagram.md`
  - `step-3.2-design-class-diagram-blueprint.md`
- `VisitorUI` is React, so it is represented only as the caller of the controller API.
- The focus here is the ASP.NET backend design flow.

## C# Code

```csharp
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading;
using System.Threading.Tasks;

namespace Comet.Phase3.UC01;

public sealed class RoomSearchController
{
    private readonly IRoomListingRepository _roomListingRepository;
    private readonly SearchMatchingService _searchMatchingService;
    private readonly IGoogleMapsGateway _googleMapsGateway;

    public RoomSearchController(
        IRoomListingRepository roomListingRepository,
        SearchMatchingService searchMatchingService,
        IGoogleMapsGateway googleMapsGateway)
    {
        _roomListingRepository = roomListingRepository;
        _searchMatchingService = searchMatchingService;
        _googleMapsGateway = googleMapsGateway;
    }

    public async Task<SearchPageResponseDto> GetSearchPageAsync(
        CancellationToken cancellationToken = default)
    {
        var listings = await _roomListingRepository.FindPublishedListingsAsync(cancellationToken);
        var summaries = _searchMatchingService.BuildListingSummaries(listings);
        var locationData = await _googleMapsGateway.GetLocationDataAsync(listings, cancellationToken);

        return new SearchPageResponseDto
        {
            Summaries = summaries,
            LocationData = locationData
        };
    }

    public async Task<SearchResponseDto> SearchRoomsAsync(
        SearchCriteriaDto criteria,
        CancellationToken cancellationToken = default)
    {
        var listings = await _roomListingRepository.FindPublishedListingsAsync(cancellationToken);
        var matchedListings = _searchMatchingService.FilterByCriteria(listings, criteria);
        var summaries = _searchMatchingService.BuildListingSummaries(matchedListings);
        var locationData = await _googleMapsGateway.GetLocationDataAsync(matchedListings, cancellationToken);

        return new SearchResponseDto
        {
            Summaries = summaries,
            LocationData = locationData,
            NoResultsMessage = matchedListings.Count == 0
                ? "No listings matched the selected criteria."
                : null
        };
    }

    public async Task<ListingEntryPointResponseDto> GetListingEntryPointAsync(
        Guid listingId,
        CancellationToken cancellationToken = default)
    {
        var listings = await _roomListingRepository.FindPublishedListingsAsync(cancellationToken);
        var listing = listings.FirstOrDefault(x => x.ListingId == listingId);

        if (listing is null)
        {
            return new ListingEntryPointResponseDto
            {
                IsFound = false,
                EntryUrl = null
            };
        }

        return new ListingEntryPointResponseDto
        {
            IsFound = true,
            EntryUrl = $"/rooms/{listingId}"
        };
    }
}

public interface IRoomListingRepository
{
    Task<List<RoomListing>> FindPublishedListingsAsync(
        CancellationToken cancellationToken = default);
}

public sealed class SearchMatchingService
{
    public List<RoomListing> FilterByCriteria(
        List<RoomListing> listings,
        SearchCriteriaDto? criteria)
    {
        if (criteria is null || criteria.IsEmpty())
        {
            return listings;
        }

        return listings
            .Where(x => MatchesLocation(x, criteria))
            .Where(x => MatchesPrice(x, criteria))
            .Where(x => MatchesCapacity(x, criteria))
            .Where(x => MatchesAvailability(x, criteria))
            .Where(x => MatchesAmenities(x, criteria))
            .ToList();
    }

    public List<ListingSummaryDto> BuildListingSummaries(List<RoomListing> listings)
    {
        return listings.Select(x => new ListingSummaryDto
        {
            ListingId = x.ListingId,
            PropertyId = x.PropertyId,
            Title = x.Title,
            Price = x.Price,
            Capacity = x.Capacity,
            AvailableFrom = x.AvailableFrom,
            FurnishedStatus = x.FurnishedStatus,
            PrivateWCStatus = x.PrivateWCStatus,
            PrimaryImageRef = x.ImagesRef
        }).ToList();
    }

    private static bool MatchesLocation(RoomListing listing, SearchCriteriaDto criteria)
    {
        if (string.IsNullOrWhiteSpace(criteria.LocationKeyword))
        {
            return true;
        }

        return listing.Title.Contains(criteria.LocationKeyword, StringComparison.OrdinalIgnoreCase)
            || listing.Description.Contains(criteria.LocationKeyword, StringComparison.OrdinalIgnoreCase);
    }

    private static bool MatchesPrice(RoomListing listing, SearchCriteriaDto criteria)
    {
        if (criteria.MaxPrice is null)
        {
            return true;
        }

        return listing.Price <= criteria.MaxPrice.Value;
    }

    private static bool MatchesCapacity(RoomListing listing, SearchCriteriaDto criteria)
    {
        if (criteria.RequiredCapacity is null)
        {
            return true;
        }

        return listing.Capacity >= criteria.RequiredCapacity.Value;
    }

    private static bool MatchesAvailability(RoomListing listing, SearchCriteriaDto criteria)
    {
        if (criteria.MoveInDate is null)
        {
            return true;
        }

        return listing.AvailableFrom <= criteria.MoveInDate.Value;
    }

    private static bool MatchesAmenities(RoomListing listing, SearchCriteriaDto criteria)
    {
        if (criteria.RequiredAmenities.Count == 0)
        {
            return true;
        }

        return criteria.RequiredAmenities.All(required => listing.Amenities.Contains(required));
    }
}

public interface IGoogleMapsGateway
{
    Task<List<LocationDataDto>> GetLocationDataAsync(
        List<RoomListing> listings,
        CancellationToken cancellationToken = default);
}

public sealed class RoomListing
{
    public Guid ListingId { get; init; }
    public Guid PropertyId { get; init; }
    public string Title { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
    public decimal Price { get; init; }
    public int Capacity { get; init; }
    public List<string> Amenities { get; init; } = new();
    public DateOnly AvailableFrom { get; init; }
    public FurnishedStatus FurnishedStatus { get; init; }
    public bool PrivateWCStatus { get; init; }
    public string ImagesRef { get; init; } = string.Empty;
    public ListingStatus Status { get; init; }
    public DateTime PublishedAt { get; init; }
}

public sealed class SearchCriteriaDto
{
    public string? LocationKeyword { get; init; }
    public decimal? MaxPrice { get; init; }
    public int? RequiredCapacity { get; init; }
    public DateOnly? MoveInDate { get; init; }
    public List<string> RequiredAmenities { get; init; } = new();

    public bool IsEmpty()
    {
        return string.IsNullOrWhiteSpace(LocationKeyword)
            && MaxPrice is null
            && RequiredCapacity is null
            && MoveInDate is null
            && RequiredAmenities.Count == 0;
    }
}

public sealed class SearchPageResponseDto
{
    public List<ListingSummaryDto> Summaries { get; init; } = new();
    public List<LocationDataDto> LocationData { get; init; } = new();
}

public sealed class SearchResponseDto
{
    public List<ListingSummaryDto> Summaries { get; init; } = new();
    public List<LocationDataDto> LocationData { get; init; } = new();
    public string? NoResultsMessage { get; init; }
}

public sealed class ListingEntryPointResponseDto
{
    public bool IsFound { get; init; }
    public string? EntryUrl { get; init; }
}

public sealed class ListingSummaryDto
{
    public Guid ListingId { get; init; }
    public Guid PropertyId { get; init; }
    public string Title { get; init; } = string.Empty;
    public decimal Price { get; init; }
    public int Capacity { get; init; }
    public DateOnly AvailableFrom { get; init; }
    public FurnishedStatus FurnishedStatus { get; init; }
    public bool PrivateWCStatus { get; init; }
    public string PrimaryImageRef { get; init; } = string.Empty;
}

public sealed class LocationDataDto
{
    public Guid ListingId { get; init; }
    public decimal Latitude { get; init; }
    public decimal Longitude { get; init; }
    public string Label { get; init; } = string.Empty;
}

public enum FurnishedStatus
{
    Unknown,
    Unfurnished,
    SemiFurnished,
    FullyFurnished
}

public enum ListingStatus
{
    Draft,
    Published,
    Hidden,
    Closed
}
```

## React Caller Shape

```csharp
// Intent only. Real UI is React, not C#.
// VisitorUI.openSearch()     -> GET /api/room-search/page
// VisitorUI.submitSearch()   -> POST /api/room-search/search
// VisitorUI.selectListing()  -> GET /api/room-search/listings/{listingId}/entry-point
```
