# ASP.NET Stack Mapping Rules

## COMET → MVC Mapping (Big Picture)

| COMET (Analysis) | COMET (Design) | MVC Layer | Example in HMSS |
|------------------|----------------|-----------|-----------------|
| `<<user interaction>>` boundary | `<<user interaction>>` | **View (V)** | `TenantUI`, `AdminUI` |
| `<<coordinator>>` / `<<state dependent control>>` | `<<coordinator>>` Controller | **Controller (C)** | `RentalRequestController` |
| `<<entity>>` (in-memory behavior) | `<<data abstraction>>` | **Model (M)** | `UserAccount`, `RoomListing` |
| `<<entity>>` (persistence) | `<<database wrapper>>` | **Model / DAO (M)** | `IUserAccountRepository` |
| `<<business logic>>` (domain helper) | `<<service>>` | **Model / Service (M)** | `AccountStatusNotificationService` |
| `<<proxy>>` | `<<proxy>>` | **Infrastructure** | `IEmailGateway`, `ICloudStorageGateway` |

> `<<data abstraction>>` is the domain Model class — owns attributes and business rules (state changes, validations).
> `<<database wrapper>>` is the Repository — loads and saves `<<data abstraction>>` objects; hides EF Core / SQL.

---

## Analysis → Design Object Mapping (Per Participant)

| Analysis stereotype | Design stereotype | Naming pattern |
|---------------------|-------------------|----------------|
| `<<user interaction>>` | `<<user interaction>>` | `<Role>UI` — e.g. `TenantUI` |
| `<<coordinator>>` (HTTP-facing) | `<<coordinator>>` | `<Entity/Feature>Controller` |
| `<<entity>>` (domain object with behavior) | `<<data abstraction>>` | `<Entity>` — e.g. `UserAccount`, `RoomListing` |
| `<<entity>>` (persistence interface) | `<<database wrapper>>` | `I<Entity>Repository` |
| `<<business logic>>` (stateless helper) | `<<service>>` | `<Purpose>Service` |
| `<<proxy>>` | `<<proxy>>` | `I<System>Gateway` |

### Standard participant set per UC

```
[Primary Actor] → <<user interaction>> UI
                         → <<coordinator>> Controller
                                → <<database wrapper>> IRepository → <<data abstraction>> DomainObject
                                → <<service>> HelperService          (only if UC needs domain logic helper)
                                → <<proxy>> IGateway → [Secondary Actor]   (only if UC touches external system)
```

---

## Analysis Message → Design Method Name Conversion

Analysis communication diagrams use noun-phrase simple messages. Design diagrams use verb-led code-style method names.

### Conversion rules

| Analysis message pattern | Design method pattern | Example |
|--------------------------|----------------------|---------|
| `<noun> request` | `get<Noun>(out response: Dto)` | `"search request"` → `getSearchResults(out response: SearchResponseDto)` |
| `provide <noun>` | `find<Nouns>(out list: List)` | `"provide published listings"` → `findPublishedListings(out listings: RoomListingList)` |
| `request <noun> page` | `get<Noun>(out response: Dto)` | `"request search page"` → `getSearchPage(out response: SearchPageResponseDto)` |
| `<noun> data` | `get<Noun>(out data: Type)` | `"location data"` → `getLocationData(out locationData: LocationData)` |
| `submit/create <noun>` | `create<Noun>(in request: Dto, out response: Dto)` | `"submit rental request"` → `createRentalRequest(in request: RentalRequestDto, out response: RentalRequestResponseDto)` |
| `update/change <noun>` | `update<Noun>(in id, in request, out response)` | `"change status"` → `changeStatus(in id: Guid, in request: Dto, out response: Dto)` |
| `cancel/delete <noun>` | `cancel<Noun>(in id, out response)` | `"cancel request"` → `cancelRentalRequest(in requestId: Guid, out response: CancelResponseDto)` |
| `approve/reject <noun>` | `approve<Noun>` / `reject<Noun>` | `"approve rental"` → `approveRentalRequest(in requestId: Guid, out response: Dto)` |
| Entity state change | `apply<Change>(in action, out result)` | business rule on domain object → `applyStatusChange(in action: ActionDto, out result: ChangeResult)` |
| load from DB | `findById(in id: Guid, out entity: Entity)` | |
| load list from DB | `findAll<Criteria>(out list: EntityList)` | `findManageableUserAccounts(out accounts: UserAccountList)` |
| save to DB | `save(in entity: Entity, out persisted: Entity)` | |
| send email (async) | `sendAsync(in message: EmailMessage)` — **no `out`** | |
| upload file (async) | `uploadAsync(in file: FileData)` — **no `out`** | |

### Naming length rule

Keep method names short and code-like. Avoid repeating the entity name unnecessarily:

| Too long | Better |
|----------|--------|
| `getUserAccountDetailInformation(...)` | `getUserAccountDetail(...)` |
| `findManageableUserAccountsFromDatabase(...)` | `findManageableUserAccounts(...)` |
| `composeStatusChangedEmailNotificationMessage(...)` | `composeStatusChangedEmail(...)` |

---

## Message-Type Decision Rules

| Caller → Receiver | Type | `out` params? |
|-------------------|------|---------------|
| UI → Controller | synchronous | yes — `out response: XxxResponseDto` |
| Controller → IRepository (read) | synchronous | yes — `out entity: Entity` or `out list: EntityList` |
| Controller → IRepository (write) | synchronous | yes — `out persisted: Entity` |
| Controller → `<<data abstraction>>` (business rule) | synchronous | yes — `out result: XxxResult` |
| Controller → Service (compute/compose) | synchronous | yes — `out result: XxxResult` |
| Controller → IGateway (fire-and-forget) | **asynchronous** | **no** |
| IGateway → External Actor | **asynchronous** | **no** |

---

## Common HMSS Type Vocabulary

| Concept | Type name |
|---------|-----------|
| Primary key | `Guid` |
| API response payload | `<UseCase>ResponseDto` |
| API request payload | `<UseCase>RequestDto` |
| Domain object (data abstraction) | `<Entity>` e.g. `UserAccount`, `RoomListing` |
| List of domain objects | `<Entity>List` |
| Status change action input | `<Entity>StatusActionDto` |
| Result of a domain state change | `<Entity>StatusChangeResult` |
| Email to dispatch | `EmailMessage` |
| File reference (cloud) | `FileReference` |
