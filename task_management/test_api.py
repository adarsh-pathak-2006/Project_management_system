from rest_framework.test import APITestCase
from register.models import User, Profile
from project.models import Project
from teams.models import Team, Member
from rest_framework.authtoken.models import Token

class APITests(APITestCase):
    def test_full_lifecycle(self):
        # 1. Register User A
        response = self.client.post('/api/auth/register/', {
            'username': 'usera',
            'email': 'a@a.com',
            'password': 'password123',
            'first_name': 'User',
            'last_name': 'A',
            'role': 'USER'
        })
        self.assertEqual(response.status_code, 201)

        # 2. Register User B
        response = self.client.post('/api/auth/register/', {
            'username': 'userb',
            'email': 'b@b.com',
            'password': 'password123',
            'first_name': 'User',
            'last_name': 'B',
            'role': 'USER'
        })
        self.assertEqual(response.status_code, 201)

        # 3. Login User A
        response = self.client.post('/api/auth/login/', {'username': 'usera', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        token_a = response.data['token']

        # 4. Login User B
        response = self.client.post('/api/auth/login/', {'username': 'userb', 'password': 'password123'})
        self.assertEqual(response.status_code, 200)
        token_b = response.data['token']

        # Set auth for User A
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_a)

        # 5. Get User A Profile
        response = self.client.get('/api/auth/profile/me/')
        self.assertEqual(response.status_code, 200)
        profile_a_id = response.data['id']

        # 6. Create Project as User A
        response = self.client.post('/api/projects/my-projects/', {
            'name': 'Project Alpha',
            'description': 'A test project'
        })
        self.assertEqual(response.status_code, 201)
        project_id = response.data['id']

        # 7. Attempt to edit Project Alpha as User B
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_b)
        response = self.client.put(f'/api/projects/my-projects/{project_id}/', {
            'name': 'Hacked Project',
            'description': 'Hacked'
        })
        self.assertEqual(response.status_code, 403)

        # 8. Create a Team as User A
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_a)
        response = self.client.post('/api/teams/', {
            'name': 'Team Alpha',
            'specialization': 'DevOps',
            'description': 'DevOps team',
            'project': [project_id]
        })
        self.assertEqual(response.status_code, 201)
        team_id = response.data['id']

        # 9. Verify User A is leader
        response = self.client.get('/api/teams/members/')
        self.assertEqual(response.status_code, 200)
        member_a = [m for m in response.data if m['team']['id'] == team_id][0]
        self.assertTrue(member_a['is_leader'])

        # 10. Attempt to edit Team as User B
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_b)
        response = self.client.put(f'/api/teams/{team_id}/', {
            'name': 'Hacked Team',
            'specialization': 'None',
            'description': 'Hacked',
            'project': []
        })
        self.assertEqual(response.status_code, 403)

        # 11. Add User B to Team as User A
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_b)
        res_b = self.client.get('/api/auth/profile/me/')
        profile_b_id = res_b.data['id']
        
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_a)
        response = self.client.post('/api/teams/members/add/', {
            'team': team_id,
            'user': profile_b_id,
            'is_leader': False
        })
        self.assertEqual(response.status_code, 201)
        member_b_id = response.data['id']

        # 12. Attempt to add another member as User B (Should fail)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_b)
        response = self.client.post('/api/teams/members/add/', {
            'team': team_id,
            'user': profile_a_id,
            'is_leader': False
        })
        self.assertEqual(response.status_code, 403)

        # 13. Attempt to delete User A as User B (Should fail)
        response = self.client.delete(f'/api/teams/members/{member_a["id"]}/')
        self.assertEqual(response.status_code, 403)

        # 14. Delete User B as User A (Should succeed)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token_a)
        response = self.client.delete(f'/api/teams/members/{member_b_id}/')
        self.assertEqual(response.status_code, 204)
