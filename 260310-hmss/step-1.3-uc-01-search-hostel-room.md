# Use Case: Search Hostel Room

## Summary

Visitor searches for available hostel room listings by entering search criteria. The system returns published listings that match the entered criteria and presents the relevant listing information to the visitor.

## Dependency

- None

## Actors

- **Primary Actor:** Visitor
- **Secondary Actor(s):** Google Maps

## Preconditions

Visitor has access to the system (no login required).

## Description of main sequence

1. Visitor accesses the room search function.
2. System displays the search form with available filter options and current published listings.
3. Visitor enters or selects desired search criteria and submits the search (location, price range, amenities, availability, move-in date).
4. System checks the submitted criteria.
5. System returns the list of published room listings that match the submitted criteria.
6. System displays the matching listings with essential information, including listing title, price, location, availability, and available map information.
7. Visitor reviews the returned listings.

## Description of alternative sequences

- **Step 3: Visitor submits with no criteria**
    - 3.1: System returns all currently published room listings using the default ordering.
    - Continues to Step 7.
- **Step 4: No listing matches the criteria**
    - 4.1: System informs the visitor that no matching room is currently available.
    - 4.2: System invites the visitor to revise the search criteria.
    - Returns to Step 3.
- **Step 6: Google Maps is unavailable**
    - 6.1: System displays the matching listings without map information.
    - Continues to Step 7.

## Nonfunctional Requirements

- **Performance:** Search results must return within 3 seconds under normal load.
- **Usability:** Filter options must be understandable to first-time users.

## Postcondition

Visitor receives a list of published room listings matching the entered criteria, or is informed that no matching listing is currently available.

## Outstanding questions

- The exact default ordering of search results when no criteria are entered will be finalized later.
