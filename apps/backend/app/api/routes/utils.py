from fastapi import APIRouter, Depends
from pydantic.networks import EmailStr

from app.api.deps import get_current_active_superuser
from app.models import Message
from app.utils import generate_test_email, send_email

router = APIRouter()


@router.post(
    "/test-email/",
    dependencies=[Depends(get_current_active_superuser)],
    status_code=201,
)
def test_email(email_to: EmailStr) -> Message:
    """
    Test emails.
    """
    email_data = generate_test_email(email_to=email_to)
    send_email(
        email_to=email_to,
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return Message(message="Test email sent")


@router.get(
    "/test/",
    status_code=200,
)
def test():
    from app.libs.ReXBole import trigger_run_recbole, trigger_run_xbole
    import os
    # from torch.utils.tensorboard import
    os.system(
        'tensorboard --logdir=log_tensorboard/BPR-ml-100k-Aug-29-2024_07-39-27-010da5/1724917185.8759904')

    # user_inputs = {
    #     'model': 'LXR',
    #     'recommender': 'CDAE-Aug-27-2024_06-19-42.pth'
    # }
    # trigger_run_xbole(user_inputs)

    return {"message": "Hello World"}
