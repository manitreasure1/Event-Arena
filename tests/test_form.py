from app.forms import Login, SignUp, Admin


def test_login_form(client):
    form = Login()
    form.email.data = "elmani@example.com"
    form.password.data = "trymewithoneword"
    assert form.validate()


def test_sign_up_form_err(client):
    form = SignUp()
    form.first_name.data = "Ava"
    form.last_name.data = "Ily"
    form.password.data = "openthis"
    assert form.validate() == False
    
def test_admin_form(client):
    form = Admin()
    form.username.data = "elmani"
    form.password.data = "trymeout"
    assert form.validate()

