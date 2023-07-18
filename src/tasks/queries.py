from src.tasks.models import Task, OwnerTaskAssociation

def get_owner_ids(task_type_name):
    if not task_type_name:
        return None, {'message': 'type_name parameter is required', 'status': 400}

    associations = OwnerTaskAssociation.query.filter_by(task_type=task_type_name).all()

    if not associations:
        return None, {'message': 'No OwnerTaskAssociations found for the given type_name', 'status': 404}

    return [association.owner_id for association in associations], None