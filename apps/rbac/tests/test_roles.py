# def test_user_without_permission_cannot_view_products(
#     user
# ):
#     client = APIClient()

#     token = ...
#     client.credentials(
#         HTTP_AUTHORIZATION=f"Bearer {token}"
#     )

#     response = client.get("/products/")

#     assert response.status_code == 403
