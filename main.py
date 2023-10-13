from server import UserView, AdsView
from app import app


app.add_url_rule("/users/", view_func=UserView.as_view("user_create"), methods=["POST"])
app.add_url_rule(
    "/users/<int:user_id>",
    view_func=UserView.as_view("users"),
    methods=["GET", "PATCH", "DELETE"],
)

app.add_url_rule("/advts/", view_func=AdsView.as_view("advt_create"), methods=["POST"])
app.add_url_rule(
    "/advts/<int:advt_id>",
    view_func=AdsView.as_view("advts"),
    methods=["GET", "PATCH", "DELETE"],
)

if __name__ == "__main__":
    app.run()
