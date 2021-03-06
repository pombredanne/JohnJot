from django.contrib.auth.models import User
from piston.handler import BaseHandler
from piston.utils import rc
from core.models import Contact
from core.models import Group
from core.models import JotDaily, JotGroup, JotContact
import logging

class ContactHandler(BaseHandler):
    """
    Handle all the requests link to the Contact model
    """
    allowed_methods = ('GET',)
    exclude = ('owner', 'date_created', 'last_edit')
    model = Contact
    
    def read(self, request, contact_id=None):
        """
        Reads all contacts, or a specific contact if `contact_id` is supplied.
        """
        queryset = Contact.objects.filter(owner=request.user)
                
        if contact_id:
            return queryset.filter(pk=contact_id)
        return queryset

class UserHandler(BaseHandler):
    """Fetch, modify, create, delete Users account. """

    allowed_methods = ('GET', 'POST') #, 'PUT', 'DELETE')

    def read(self, request, username):

        user = self.user_exists(username)
        if user is not None:
            return user
        else:
            response = rc.NOT_FOUND
            response.write('%s does\'t exist.' % username)
            return response
    
    def create(self, request):
        """Create new users."""
        
        req = request.POST
        username = req.get('username')
        password = req.get('password')
        email = req.get('email')

        if not username:
            response = rc.BAD_REQUEST
            response.write('Missing Username')
            return response

        if not password:
            response = rc.BAD_REQUEST
            response.write('Missing Password')
            return response

        if not email:
            response = rc.BAD_REQUEST
            response.write('Missing Email')
            return response

        if self.user_exists(username) is not None:
            response = rc.DUPLICATE_ENTRY
            response.write('User already exists.')
            return response
        else:
            new_user = User.objects.create_user(username, email, password)
            response = rc.CREATED
            response.write('User %s has been created.' % new_user.username)
            return response
 
    def user_exists(self, username):
        """Verifies if username is taken."""
        try:
            user = User.objects.get(username=username)
            return user
        except User.DoesNotExist:
            return None



class GroupHandler(BaseHandler):
    """
    Handle all the requests link to the Group model
    """
    allowed_methods = ('GET',)
    exclude = ('owner', 'date_created', 'last_edit')
    model = Group
    
    def read(self, request, group_id=None):
        """
        Reads all groups, or a specific group if` group_id` is supplied.
        """
        queryset = Group.objects.filter(owner=request.user)
                
        if group_id:
            return queryset.filter(pk=group_id)
        return queryset

class JotDailyHandler(BaseHandler):
    """
    Handle all the requests link to the JotDaily model
    """
    allowed_methods = ('GET',)
    exclude = ('owner', 'date_created', 'last_edit')
    model = JotDaily

    def read(self, request, jot_id=None):
        """
        Reads all daily_jots, or a specific daily_jot if` jot_id` is supplied.
        """
        queryset = JotDaily.objects.filter(owner=request.user)
                
        if jot_id:
            return queryset.filter(pk=jot_id)
        return queryset

class JotContactHandler(BaseHandler):
    """
    Handle all the requests link to the JotContact model
    """
    allowed_methods = ('GET',)
    exclude = ('date_created', 'last_edit')
    model = JotContact

    def read(self, request, contact_id=None):
        """
        Reads all contact_jots, 
        or all the jots link to a contact if `contact_id` is supplied.
        """
        contacts = Contact.objects.filter(owner=request.user)
        queryset = JotContact.objects.filter(contact__in=contacts)
                
        if contact_id:
            return queryset.filter(contact=contact_id)
        return queryset

class JotGroupHandler(BaseHandler):
    """
    Handle all the requests link to the JotGroup model
    """
    allowed_methods = ('GET',)
    exclude = ('date_created', 'last_edit')
    model = JotGroup

    def read(self, request, group_id=None):
        """
        Reads all group_jots,
        or all the jots link to a group if `group_id` is supplied.
        """
        groups = Group.objects.filter(owner=request.user)
        queryset = JotGroup.objects.filter(group__in=groups)
                
        if group_id:
            return queryset.filter(group=group_id)
        return queryset
