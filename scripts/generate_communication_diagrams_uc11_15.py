#!/usr/bin/env python3
"""
Generate draw.io communication diagrams for UC-11 through UC-15
based on their markdown blueprint specifications.
"""

import os
import re
from pathlib import Path

# Base paths
BASE_DIR = Path(r"C:\Users\welterial\commet")
PHASE2_DIR = BASE_DIR / "260310-hmss" / "phase-2"

# Diagram specifications for UC-11 through UC-15
DIAGRAMS = {
    "uc-11": {
        "markdown": "step-2.2-uc-11-publish-room-listing-main-seq.md",
        "drawio": "step-2.2-uc-11-publish-room-listing-main-seq.drawio",
        "title": "UC-11 Publish Room Listing - Main Sequence",
        "id": "uc-11-publish-room-listing",
        "layout": """Owner --- OwnerUI --- PublishListingCoordinator --- PublicationRules --- RoomListing
                                                         |
                                                         --- OwnerProfile""",
        "participants": [
            {"name": "Owner", "type": "actor", "position": (60, 310), "size": (50, 90)},
            {"name": "OwnerUI", "stereotype": "user interaction", "position": (180, 320), "size": (200, 70)},
            {"name": "PublishListingCoordinator", "stereotype": "coordinator", "position": (460, 320), "size": (230, 70)},
            {"name": "PublicationRules", "stereotype": "business logic", "position": (760, 150), "size": (190, 70)},
            {"name": "RoomListing", "stereotype": "entity", "position": (1010, 150), "size": (160, 70)},
            {"name": "OwnerProfile", "stereotype": "entity", "position": (1010, 320), "size": (170, 70)},
        ],
        "associations": [
            ("Owner", "OwnerUI"),
            ("OwnerUI", "PublishListingCoordinator"),
            ("PublishListingCoordinator", "PublicationRules"),
            ("PublicationRules", "RoomListing"),
            ("PublicationRules", "OwnerProfile"),
        ],
        "messages": [
            {"num": "1", "from": "Owner", "to": "OwnerUI", "text": "Publication Access", "pos": (70, 200)},
            {"num": "1.1", "from": "OwnerUI", "to": "PublishListingCoordinator", "text": "Listing Detail Request", "pos": (250, 200)},
            {"num": "1.2", "from": "PublishListingCoordinator", "to": "PublicationRules", "text": "Listing Detail Query", "pos": (530, 100)},
            {"num": "1.3", "from": "PublicationRules", "to": "RoomListing", "text": "Listing Detail Query", "pos": (820, 100)},
            {"num": "1.4", "from": "RoomListing", "to": "PublicationRules", "text": "Listing Data", "pos": (820, 125)},
            {"num": "1.5", "from": "PublicationRules", "to": "PublishListingCoordinator", "text": "Listing Data", "pos": (530, 125)},
            {"num": "1.6", "from": "PublishListingCoordinator", "to": "OwnerUI", "text": "Listing Data and Checklist", "pos": (250, 225)},
            {"num": "1.7", "from": "OwnerUI", "to": "Owner", "text": "Listing and Checklist Display", "pos": (70, 225)},
            {"num": "2", "from": "Owner", "to": "OwnerUI", "text": "Publication Request", "pos": (70, 400)},
            {"num": "2.1", "from": "OwnerUI", "to": "PublishListingCoordinator", "text": "Publication Evaluation Request", "pos": (250, 400)},
            {"num": "2.2", "from": "PublishListingCoordinator", "to": "PublicationRules", "text": "Eligibility Check (Listing & Owner Data)", "pos": (530, 250)},
            {"num": "2.3", "from": "PublicationRules", "to": "PublishListingCoordinator", "text": "Eligibility Result (Eligible)", "pos": (530, 275)},
            {"num": "2.4", "from": "PublishListingCoordinator", "to": "OwnerUI", "text": "Publication Confirmation Prompt", "pos": (250, 425)},
            {"num": "2.5", "from": "OwnerUI", "to": "Owner", "text": "Confirmation Prompt Display", "pos": (70, 425)},
            {"num": "3", "from": "Owner", "to": "OwnerUI", "text": "Publication Confirmation", "pos": (70, 600)},
            {"num": "3.1", "from": "OwnerUI", "to": "PublishListingCoordinator", "text": "Confirmed Publication", "pos": (250, 600)},
            {"num": "3.2", "from": "PublishListingCoordinator", "to": "RoomListing", "text": "Published Status Update", "pos": (820, 190)},
            {"num": "3.3", "from": "PublishListingCoordinator", "to": "OwnerUI", "text": "Publication Success", "pos": (250, 625)},
            {"num": "3.4", "from": "OwnerUI", "to": "Owner", "text": "Publication Success Message", "pos": (70, 625)},
        ]
    },
    "uc-12": {
        "markdown": "step-2.2-uc-12-change-listing-visibility-main-seq.md",
        "drawio": "step-2.2-uc-12-change-listing-visibility-main-seq.drawio",
        "title": "UC-12 Change Listing Visibility - Main Sequence",
        "id": "uc-12-change-listing-visibility",
        "layout": """Owner --- OwnerUI --- ChangeVisibilityCoordinator --- VisibilityRules --- RoomListing""",
        "participants": [
            {"name": "Owner", "type": "actor", "position": (60, 310), "size": (50, 90)},
            {"name": "OwnerUI", "stereotype": "user interaction", "position": (180, 320), "size": (210, 70)},
            {"name": "ChangeVisibilityCoordinator", "stereotype": "coordinator", "position": (450, 320), "size": (250, 70)},
            {"name": "VisibilityRules", "stereotype": "business logic", "position": (760, 320), "size": (180, 70)},
            {"name": "RoomListing", "stereotype": "entity", "position": (1010, 320), "size": (160, 70)},
        ],
        "associations": [
            ("Owner", "OwnerUI"),
            ("OwnerUI", "ChangeVisibilityCoordinator"),
            ("ChangeVisibilityCoordinator", "VisibilityRules"),
            ("VisibilityRules", "RoomListing"),
        ],
        "messages": [
            {"num": "1", "from": "Owner", "to": "OwnerUI", "text": "Listing Selection", "pos": (70, 180)},
            {"num": "1.1", "from": "OwnerUI", "to": "ChangeVisibilityCoordinator", "text": "Listing Detail Request", "pos": (260, 180)},
            {"num": "1.2", "from": "ChangeVisibilityCoordinator", "to": "VisibilityRules", "text": "Listing Detail Query", "pos": (560, 180)},
            {"num": "1.3", "from": "VisibilityRules", "to": "RoomListing", "text": "Listing Detail Query", "pos": (820, 180)},
            {"num": "1.4", "from": "RoomListing", "to": "VisibilityRules", "text": "Listing Data", "pos": (820, 205)},
            {"num": "1.5", "from": "VisibilityRules", "to": "ChangeVisibilityCoordinator", "text": "Listing Data", "pos": (560, 205)},
            {"num": "1.6", "from": "ChangeVisibilityCoordinator", "to": "OwnerUI", "text": "Listing Data and Visibility Actions", "pos": (260, 205)},
            {"num": "1.7", "from": "OwnerUI", "to": "Owner", "text": "Listing Details and Actions Display", "pos": (70, 205)},
            {"num": "2", "from": "Owner", "to": "OwnerUI", "text": "Visibility Action Selection", "pos": (70, 380)},
            {"num": "2.1", "from": "OwnerUI", "to": "ChangeVisibilityCoordinator", "text": "Visibility Action Request", "pos": (260, 380)},
            {"num": "2.2", "from": "ChangeVisibilityCoordinator", "to": "VisibilityRules", "text": "Action Validity Check", "pos": (560, 260)},
            {"num": "2.3", "from": "VisibilityRules", "to": "ChangeVisibilityCoordinator", "text": "Validity Result (Valid)", "pos": (560, 285)},
            {"num": "2.4", "from": "ChangeVisibilityCoordinator", "to": "OwnerUI", "text": "Visibility Confirmation Prompt", "pos": (260, 405)},
            {"num": "2.5", "from": "OwnerUI", "to": "Owner", "text": "Confirmation Prompt Display", "pos": (70, 405)},
            {"num": "3", "from": "Owner", "to": "OwnerUI", "text": "Visibility Change Confirmation", "pos": (70, 580)},
            {"num": "3.1", "from": "OwnerUI", "to": "ChangeVisibilityCoordinator", "text": "Confirmed Visibility Change", "pos": (260, 580)},
            {"num": "3.2", "from": "ChangeVisibilityCoordinator", "to": "RoomListing", "text": "Visibility Status Update", "pos": (820, 270)},
            {"num": "3.3", "from": "ChangeVisibilityCoordinator", "to": "OwnerUI", "text": "Visibility Change Success", "pos": (260, 605)},
            {"num": "3.4", "from": "OwnerUI", "to": "Owner", "text": "Visibility Success Message", "pos": (70, 605)},
        ]
    },
    "uc-13": {
        "markdown": "step-2.2-uc-13-submit-owner-verification-main-seq.md",
        "drawio": "step-2.2-uc-13-submit-owner-verification-main-seq.drawio",
        "title": "UC-13 Submit Owner Verification - Main Sequence",
        "id": "uc-13-submit-owner-verification",
        "layout": """Owner --- OwnerUI --- SubmitVerificationCoordinator --- VerificationRules --- OwnerVerification
                                      |
                                      --- CloudStorageProxy --- Cloud Storage""",
        "participants": [
            {"name": "Owner", "type": "actor", "position": (60, 310), "size": (50, 90)},
            {"name": "OwnerUI", "stereotype": "user interaction", "position": (180, 320), "size": (200, 70)},
            {"name": "SubmitVerificationCoordinator", "stereotype": "coordinator", "position": (440, 320), "size": (260, 70)},
            {"name": "VerificationRules", "stereotype": "business logic", "position": (760, 150), "size": (200, 70)},
            {"name": "OwnerVerification", "stereotype": "entity", "position": (1020, 150), "size": (190, 70)},
            {"name": "CloudStorageProxy", "stereotype": "proxy", "position": (760, 480), "size": (190, 70)},
            {"name": "Cloud Storage", "type": "actor", "position": (1020, 470), "size": (60, 90)},
        ],
        "associations": [
            ("Owner", "OwnerUI"),
            ("OwnerUI", "SubmitVerificationCoordinator"),
            ("SubmitVerificationCoordinator", "VerificationRules"),
            ("VerificationRules", "OwnerVerification"),
            ("SubmitVerificationCoordinator", "CloudStorageProxy"),
            ("CloudStorageProxy", "Cloud Storage"),
        ],
        "messages": [
            {"num": "1", "from": "Owner", "to": "OwnerUI", "text": "Verification Access", "pos": (70, 180)},
            {"num": "1.1", "from": "OwnerUI", "to": "SubmitVerificationCoordinator", "text": "Verification Form Request", "pos": (250, 180)},
            {"num": "1.2", "from": "SubmitVerificationCoordinator", "to": "OwnerUI", "text": "Verification Form", "pos": (250, 205)},
            {"num": "1.3", "from": "OwnerUI", "to": "Owner", "text": "Form Display", "pos": (70, 205)},
            {"num": "2", "from": "Owner", "to": "OwnerUI", "text": "Information and Documents Input", "pos": (70, 380)},
            {"num": "2.1", "from": "OwnerUI", "to": "SubmitVerificationCoordinator", "text": "Validation and Upload Request", "pos": (250, 380)},
            {"num": "2.2", "from": "SubmitVerificationCoordinator", "to": "VerificationRules", "text": "Required Fields Validation Check", "pos": (530, 100)},
            {"num": "2.3", "from": "VerificationRules", "to": "SubmitVerificationCoordinator", "text": "Validation Result (Valid)", "pos": (530, 125)},
            {"num": "2.4", "from": "SubmitVerificationCoordinator", "to": "CloudStorageProxy", "text": "Document Upload Request", "pos": (530, 430)},
            {"num": "2.5", "from": "CloudStorageProxy", "to": "Cloud Storage", "text": "Document Upload", "pos": (820, 430)},
            {"num": "2.6", "from": "Cloud Storage", "to": "CloudStorageProxy", "text": "Upload Confirmation", "pos": (820, 455)},
            {"num": "2.7", "from": "CloudStorageProxy", "to": "SubmitVerificationCoordinator", "text": "Upload Result (Success)", "pos": (530, 455)},
            {"num": "2.8", "from": "SubmitVerificationCoordinator", "to": "OwnerUI", "text": "Review Prompt", "pos": (250, 405)},
            {"num": "2.9", "from": "OwnerUI", "to": "Owner", "text": "Verification Review Display", "pos": (70, 405)},
            {"num": "3", "from": "Owner", "to": "OwnerUI", "text": "Submission Confirmation", "pos": (70, 580)},
            {"num": "3.1", "from": "OwnerUI", "to": "SubmitVerificationCoordinator", "text": "Submission Request", "pos": (250, 580)},
            {"num": "3.2", "from": "SubmitVerificationCoordinator", "to": "OwnerVerification", "text": "New Verification Record", "pos": (820, 190)},
            {"num": "3.3", "from": "SubmitVerificationCoordinator", "to": "OwnerUI", "text": "Submission Success", "pos": (250, 605)},
            {"num": "3.4", "from": "OwnerUI", "to": "Owner", "text": "Success Message", "pos": (70, 605)},
        ]
    },
    "uc-14": {
        "markdown": "step-2.2-uc-14-review-rental-request-main-seq.md",
        "drawio": "step-2.2-uc-14-review-rental-request-main-seq.drawio",
        "title": "UC-14 Review Rental Request - Main Sequence",
        "id": "uc-14-review-rental-request",
        "layout": """Owner --- OwnerUI --- ReviewRequestCoordinator --- ReviewRequestRules --- RentalRequest
                                      |                         |
                                      |                         --- RoomListing
                                      |
                                      --- EmailProxy --- Email Provider""",
        "participants": [
            {"name": "Owner", "type": "actor", "position": (60, 380), "size": (50, 90)},
            {"name": "OwnerUI", "stereotype": "user interaction", "position": (180, 390), "size": (180, 70)},
            {"name": "ReviewRequestCoordinator", "stereotype": "coordinator", "position": (420, 390), "size": (230, 70)},
            {"name": "ReviewRequestRules", "stereotype": "business logic", "position": (710, 150), "size": (200, 70)},
            {"name": "RentalRequest", "stereotype": "entity", "position": (980, 150), "size": (170, 70)},
            {"name": "RoomListing", "stereotype": "entity", "position": (980, 320), "size": (160, 70)},
            {"name": "EmailProxy", "stereotype": "proxy", "position": (710, 580), "size": (170, 70)},
            {"name": "Email Provider", "type": "actor", "position": (940, 570), "size": (70, 90)},
        ],
        "associations": [
            ("Owner", "OwnerUI"),
            ("OwnerUI", "ReviewRequestCoordinator"),
            ("ReviewRequestCoordinator", "ReviewRequestRules"),
            ("ReviewRequestRules", "RentalRequest"),
            ("ReviewRequestRules", "RoomListing"),
            ("ReviewRequestCoordinator", "EmailProxy"),
            ("EmailProxy", "Email Provider"),
        ],
        "messages": [
            {"num": "1", "from": "Owner", "to": "OwnerUI", "text": "Review Function Access", "pos": (70, 180)},
            {"num": "1.1", "from": "OwnerUI", "to": "ReviewRequestCoordinator", "text": "Room Requests Query", "pos": (240, 180)},
            {"num": "1.2", "from": "ReviewRequestCoordinator", "to": "ReviewRequestRules", "text": "Room Requests Data Request", "pos": (530, 100)},
            {"num": "1.3", "from": "ReviewRequestRules", "to": "RentalRequest", "text": "Room Requests Data Request", "pos": (800, 100)},
            {"num": "1.4", "from": "RentalRequest", "to": "ReviewRequestRules", "text": "Room Requests Data", "pos": (800, 125)},
            {"num": "1.5", "from": "ReviewRequestRules", "to": "ReviewRequestCoordinator", "text": "Room Requests Data", "pos": (530, 125)},
            {"num": "1.6", "from": "ReviewRequestCoordinator", "to": "OwnerUI", "text": "Room Requests List", "pos": (240, 205)},
            {"num": "1.7", "from": "OwnerUI", "to": "Owner", "text": "Requests Display", "pos": (70, 205)},
            {"num": "2", "from": "Owner", "to": "OwnerUI", "text": "Request Selection", "pos": (70, 380)},
            {"num": "2.1", "from": "OwnerUI", "to": "ReviewRequestCoordinator", "text": "Request Detail Query", "pos": (240, 380)},
            {"num": "2.2", "from": "ReviewRequestCoordinator", "to": "ReviewRequestRules", "text": "Request Detail Request", "pos": (530, 260)},
            {"num": "2.3", "from": "ReviewRequestRules", "to": "RentalRequest", "text": "Request Detail Request", "pos": (800, 150)},
            {"num": "2.4", "from": "RentalRequest", "to": "ReviewRequestRules", "text": "Request Detail Data", "pos": (800, 175)},
            {"num": "2.5", "from": "ReviewRequestRules", "to": "ReviewRequestCoordinator", "text": "Request Detail Data", "pos": (530, 285)},
            {"num": "2.6", "from": "ReviewRequestCoordinator", "to": "OwnerUI", "text": "Request Detail and Options", "pos": (240, 405)},
            {"num": "2.7", "from": "OwnerUI", "to": "Owner", "text": "Request Detail Display", "pos": (70, 405)},
            {"num": "3", "from": "Owner", "to": "OwnerUI", "text": "Acceptance Decision", "pos": (70, 580)},
            {"num": "3.1", "from": "OwnerUI", "to": "ReviewRequestCoordinator", "text": "Acceptance Request", "pos": (240, 580)},
            {"num": "3.2", "from": "ReviewRequestCoordinator", "to": "ReviewRequestRules", "text": "Decision Validation Check", "pos": (530, 460)},
            {"num": "3.3", "from": "ReviewRequestRules", "to": "ReviewRequestCoordinator", "text": "Validation Result (Valid)", "pos": (530, 485)},
            {"num": "3.4", "from": "ReviewRequestCoordinator", "to": "RentalRequest", "text": "Accepted Status Update", "pos": (800, 200)},
            {"num": "3.5", "from": "ReviewRequestCoordinator", "to": "RoomListing", "text": "Locked Status Update", "pos": (800, 330)},
            {"num": "3.6", "from": "ReviewRequestCoordinator", "to": "EmailProxy", "text": "Tenant Notification Request", "pos": (530, 530)},
            {"num": "3.7", "from": "EmailProxy", "to": "Email Provider", "text": "Tenant Notification", "pos": (800, 530)},
            {"num": "3.8", "from": "ReviewRequestCoordinator", "to": "OwnerUI", "text": "Decision Success", "pos": (240, 605)},
            {"num": "3.9", "from": "OwnerUI", "to": "Owner", "text": "Success Message Display", "pos": (70, 605)},
        ]
    },
    "uc-15": {
        "markdown": "step-2.2-uc-15-reopen-room-listing-main-seq.md",
        "drawio": "step-2.2-uc-15-reopen-room-listing-main-seq.drawio",
        "title": "UC-15 Reopen Room Listing - Main Sequence",
        "id": "uc-15-reopen-room-listing",
        "layout": """Owner --- OwnerUI --- ReopenRoomCoordinator --- ReopenRules --- RentalRequest
                                      |                     |
                                      |                     --- RoomListing
                                      |
                                      --- EmailProxy --- Email Provider""",
        "participants": [
            {"name": "Owner", "type": "actor", "position": (60, 380), "size": (50, 90)},
            {"name": "OwnerUI", "stereotype": "user interaction", "position": (180, 390), "size": (170, 70)},
            {"name": "ReopenRoomCoordinator", "stereotype": "coordinator", "position": (410, 390), "size": (210, 70)},
            {"name": "ReopenRules", "stereotype": "business logic", "position": (680, 150), "size": (170, 70)},
            {"name": "RentalRequest", "stereotype": "entity", "position": (920, 150), "size": (170, 70)},
            {"name": "RoomListing", "stereotype": "entity", "position": (920, 320), "size": (190, 70)},
            {"name": "EmailProxy", "stereotype": "proxy", "position": (680, 580), "size": (160, 70)},
            {"name": "Email Provider", "type": "actor", "position": (900, 570), "size": (70, 90)},
        ],
        "associations": [
            ("Owner", "OwnerUI"),
            ("OwnerUI", "ReopenRoomCoordinator"),
            ("ReopenRoomCoordinator", "ReopenRules"),
            ("ReopenRules", "RentalRequest"),
            ("ReopenRules", "RoomListing"),
            ("ReopenRoomCoordinator", "EmailProxy"),
            ("EmailProxy", "Email Provider"),
        ],
        "messages": [
            {"num": "1", "from": "Owner", "to": "OwnerUI", "text": "Accepted Arrangements Access", "pos": (70, 180)},
            {"num": "1.1", "from": "OwnerUI", "to": "ReopenRoomCoordinator", "text": "Accepted Arrangements Query", "pos": (230, 180)},
            {"num": "1.2", "from": "ReopenRoomCoordinator", "to": "ReopenRules", "text": "Accepted Arrangements Request", "pos": (500, 100)},
            {"num": "1.3", "from": "ReopenRules", "to": "RentalRequest", "text": "Accepted Arrangements Request", "pos": (760, 100)},
            {"num": "1.4", "from": "RentalRequest", "to": "ReopenRules", "text": "Accepted Arrangements Data", "pos": (760, 125)},
            {"num": "1.5", "from": "ReopenRules", "to": "ReopenRoomCoordinator", "text": "Accepted Arrangements Data", "pos": (500, 125)},
            {"num": "1.6", "from": "ReopenRoomCoordinator", "to": "OwnerUI", "text": "Accepted Arrangements and Room Info", "pos": (230, 205)},
            {"num": "1.7", "from": "OwnerUI", "to": "Owner", "text": "Arrangements Display", "pos": (70, 205)},
            {"num": "2", "from": "Owner", "to": "OwnerUI", "text": "Arrangement Selection", "pos": (70, 380)},
            {"num": "2.1", "from": "OwnerUI", "to": "ReopenRoomCoordinator", "text": "Arrangement Selection Request", "pos": (230, 380)},
            {"num": "2.2", "from": "ReopenRoomCoordinator", "to": "ReopenRules", "text": "Status Concurrency Check", "pos": (500, 260)},
            {"num": "2.3", "from": "ReopenRules", "to": "RentalRequest", "text": "Request Status Query", "pos": (760, 150)},
            {"num": "2.4", "from": "RentalRequest", "to": "ReopenRules", "text": "Request Status Data", "pos": (760, 175)},
            {"num": "2.5", "from": "ReopenRules", "to": "ReopenRoomCoordinator", "text": "Validation Result (Valid)", "pos": (500, 285)},
            {"num": "2.6", "from": "ReopenRoomCoordinator", "to": "OwnerUI", "text": "Reopen Action Prompt and Consequences", "pos": (230, 405)},
            {"num": "2.7", "from": "OwnerUI", "to": "Owner", "text": "Prompt Display", "pos": (70, 405)},
            {"num": "3", "from": "Owner", "to": "OwnerUI", "text": "Reopen Confirmation", "pos": (70, 580)},
            {"num": "3.1", "from": "OwnerUI", "to": "ReopenRoomCoordinator", "text": "Confirmed Reopen Request", "pos": (230, 580)},
            {"num": "3.2", "from": "ReopenRoomCoordinator", "to": "RentalRequest", "text": "Revoked Status Update", "pos": (760, 200)},
            {"num": "3.3", "from": "ReopenRoomCoordinator", "to": "RoomListing", "text": "Published Available Status Update", "pos": (760, 330)},
            {"num": "3.4", "from": "ReopenRoomCoordinator", "to": "EmailProxy", "text": "Tenant Notification Request", "pos": (500, 530)},
            {"num": "3.5", "from": "EmailProxy", "to": "Email Provider", "text": "Tenant Notification", "pos": (760, 530)},
            {"num": "3.6", "from": "ReopenRoomCoordinator", "to": "OwnerUI", "text": "Reopen Success", "pos": (230, 605)},
            {"num": "3.7", "from": "OwnerUI", "to": "Owner", "text": "Reopen Success Message", "pos": (70, 605)},
        ]
    },
}


def sanitize_id(name: str) -> str:
    """Convert a name to a valid XML ID."""
    return name.lower().replace(" ", "-").replace("_", "-")


def generate_participant_xml(p: dict, idx: int) -> str:
    """Generate XML for a participant (actor or object)."""
    pid = f"obj-{sanitize_id(p['name'])}-{idx}"

    if p.get("type") == "actor":
        # Actor shape
        value = p["name"]
        style = "shape=umlActor;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;verticalLabelPosition=bottom;verticalAlign=top;align=center;"
        x, y = p["position"]
        w, h = p["size"]
    else:
        # Software object
        stereotype = f"&#171;{p['stereotype']}&#187;"
        value = f"{stereotype}&lt;br/&gt;: {p['name']}"
        style = "rounded=0;whiteSpace=wrap;html=1;fillColor=#82CAFA;strokeColor=#000000;align=center;verticalAlign=middle;fontColor=#000000;"
        x, y = p["position"]
        w, h = p["size"]

    return f'''        <mxCell id="{pid}" value="{value}" style="{style}" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/>
        </mxCell>'''


def generate_association_xml(from_name: str, to_name: str, idx: int) -> str:
    """Generate XML for an undirected association."""
    aid = f"assoc-{sanitize_id(from_name)}-{sanitize_id(to_name)}"
    from_id = f"obj-{sanitize_id(from_name)}-0"
    to_id = f"obj-{sanitize_id(to_name)}-0"

    return f'''        <mxCell id="{aid}" style="edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;endArrow=none;startArrow=none;strokeColor=#000000;" edge="1" parent="1" source="{from_id}" target="{to_id}">
          <mxGeometry relative="1" as="geometry"/>
        </mxCell>'''


def generate_message_xml(msg: dict) -> str:
    """Generate XML for a message (text box + arrow)."""
    msg_id = f"msg-{msg['num'].replace('.', '-')}"
    x, y = msg["pos"]

    # Calculate approximate width based on text length
    text_len = len(msg["text"])
    width = max(150, min(300, text_len * 8))
    height = 24

    # Determine arrow direction based on participant positions
    # For simplicity, we'll use a short horizontal arrow
    arrow_len = 40
    arrow_x = x + width + 10
    arrow_y = y + height // 2

    return f'''        <mxCell id="{msg_id}" value="{msg['num']}: {msg['text']}" style="text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontColor=#000000;" vertex="1" parent="1">
          <mxGeometry x="{x}" y="{y}" width="{width}" height="{height}" as="geometry"/>
        </mxCell>
        <mxCell id="{msg_id}-arrow" style="edgeStyle=none;rounded=0;html=1;endArrow=classic;startArrow=none;strokeColor=#000000;" edge="1" parent="1">
          <mxGeometry relative="1" as="geometry">
            <mxPoint x="{x + width + 10}" y="{arrow_y}" as="sourcePoint"/>
            <mxPoint x="{x + width + 10 + arrow_len}" y="{arrow_y}" as="targetPoint"/>
          </mxGeometry>
        </mxCell>'''


def generate_diagram_xml(diagram_key: str) -> str:
    """Generate complete draw.io XML for a diagram."""
    spec = DIAGRAMS[diagram_key]

    # Build participants
    participants_xml = "\n".join([
        generate_participant_xml(p, i)
        for i, p in enumerate(spec["participants"])
    ])

    # Build associations
    associations_xml = "\n".join([
        generate_association_xml(from_p, to_p, i)
        for i, (from_p, to_p) in enumerate(spec["associations"])
    ])

    # Build messages
    messages_xml = "\n".join([
        generate_message_xml(msg)
        for msg in spec["messages"]
    ])

    # Complete document
    xml = f'''<mxfile host="app.diagrams.net" version="26.0.11">
  <diagram id="{spec['id']}" name="{spec['title']}">
    <mxGraphModel dx="1400" dy="980" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="1500" pageHeight="1100" math="0" shadow="0">
      <root>
        <mxCell id="0"/>
        <mxCell id="1" parent="0"/>
{participants_xml}
{associations_xml}
{messages_xml}
      </root>
    </mxGraphModel>
  </diagram>
</mxfile>'''

    return xml


def main():
    """Generate all diagrams."""
    for diagram_key in ["uc-11", "uc-12", "uc-13", "uc-14", "uc-15"]:
        spec = DIAGRAMS[diagram_key]
        output_path = PHASE2_DIR / spec["drawio"]

        print(f"Generating {spec['drawio']}...")

        xml = generate_diagram_xml(diagram_key)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml)

        print(f"  ✓ Generated: {output_path}")

    print("\nAll diagrams generated successfully!")


if __name__ == "__main__":
    main()
