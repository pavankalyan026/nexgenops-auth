from sqlalchemy.orm import Session
from database.models import Organization


def generate_organization_id(
    db: Session
):

    count = db.query(
        Organization
    ).count()

    next_id = count + 1

    return f"ORG{next_id:06d}"