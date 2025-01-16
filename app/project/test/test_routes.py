# from app.accounts.factories import UserFactory
# from app.project.factories import ProjectFactory, Project
# from app.test.base import BaseTest
# from fastapi import status
# from datetime import datetime


# class TestProject(BaseTest):
#     def test_create_project(self):
#         self.force_authenticate(user=None)
#         data = {
#             "title": "string",
#             "description": "",
#             "goal_amount": 1,
#             "deadline": "2025-01-15T23:10:58.689Z"
#         }

#         response = self.client.post("/projects/", json=data)

#         assert response.status_code == status.HTTP_403_FORBIDDEN

#         user = UserFactory()
#         self.force_authenticate(user=user)

#         response = self.client.post("/projects/", json=data)

#         assert response.status_code == status.HTTP_200_OK

#         created_project = response.json()
#         assert created_project["title"] == data["title"]

#     def test_get_project(self):
#         user = UserFactory()
#         self.force_authenticate(user=user)

#         project = ProjectFactory()
#         response = self.client.get(f"/projects/{project.id}")
#         assert response.status_code == status.HTTP_200_OK

#         data = response.json()
#         assert data["title"] == project.title

#     def test_get_all_projects(self):
#         user = UserFactory()
#         self.force_authenticate(user=user)

#         ProjectFactory.create_batch(2)

#         response = self.client.get("/projects/")
#         assert response.status_code == status.HTTP_200_OK

#         data = response.json()
#         assert len(data["items"]) == 2

#     def test_update_projects(self):
#         user = UserFactory()
#         self.force_authenticate(user=user)

#         project = ProjectFactory()

#         updated_data = {
#             "title": "Test project",
#             "description": "test@project.com",
#             "deadline": str(datetime.now())
#         }

#         response = self.client.put(
#             f"/projects/{project.id}", json=updated_data
#         )

#         assert response.status_code == status.HTTP_200_OK

#         updated_project = response.json()
#         assert updated_project["title"] == updated_data["title"]

#     def test_delete_project(self):
#         user = UserFactory()
#         self.force_authenticate(user=user)

#         project = ProjectFactory()

#         response = self.client.delete(f"/projects/{project.id}")
#         assert response.status_code == status.HTTP_200_OK

#         response = self.client.get(f"/projects/{project.id}")
#         assert response.status_code == status.HTTP_404_NOT_FOUND
