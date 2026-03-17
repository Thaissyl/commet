# Class Interface Specification: IRoomListingRepository

## Class Summary

- Stereotype: `<<database wrapper>>`
- Scope: `UC-02 View Room Details - ASP.NET simple layered backend`
- Hidden Information: EF Core query implementation, SQL joins between RoomListing and Property tables, and database connection management
- Structuring Criterion: database wrapper

## Assumptions

- The repository implementation performs a join to include property name and address in the returned `RoomListing` object so the controller does not need a separate property lookup.
- The interface is defined in the domain layer; the EF Core implementation resides in the infrastructure layer.

## Anticipated Changes

- Additional filter or projection overloads may be added as new use cases require different listing queries.
- A caching layer may be introduced in the implementation without changing the interface contract.

## Private Attributes

- None in current scope.

## Invariants

- Must not embed business rules or visibility logic; visibility filtering is the controller's responsibility.
- Must not expose raw SQL or ORM types through the interface.

## Collaborators

- `RoomDetailController`: the sole caller in this UC scope

## Operations Provided

### `+ findById(in listingId: Guid, out listing: RoomListing)`

- Source communication messages: `1.2`
- Function: Loads a single room listing record by its identifier, including joined property name and address data.
- Parameters:
  - `in listingId`: identifier of the requested listing
  - `out listing`: the loaded `RoomListing` domain object, or null if not found
- Preconditions:
  - Database is accessible.
- Postconditions:
  - If a record exists for `listingId`, `listing` is populated with all room and property fields.
  - If no record exists, `listing` is null.

## Operations Required

- None in current scope.

## Traceability

- Source use case: `UC-02 View Room Details`
- Source design communication messages:
  - `1.2 RoomDetailController -> IRoomListingRepository`
