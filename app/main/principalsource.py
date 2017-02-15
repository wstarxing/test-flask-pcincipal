# -*- coding: UTF-8 -*-
from collections import namedtuple
from functools import partial


from flask_principal import Principal, Identity, AnonymousIdentity, \
    identity_changed, identity_loaded, RoleNeed, UserNeed, Permission

BlogPostNeed = namedtuple('blog_post', ['method', 'value'])
EditBlogPostNeed = partial(BlogPostNeed, 'edit')


class EditBlogPostPermission(Permission):
    def __init__(self, post_id):
        need = EditBlogPostNeed(unicode(post_id))
        super(EditBlogPostPermission, self).__init__(need)


admin_permission = Permission(RoleNeed('admin'))
vip_permission = Permission(RoleNeed('vip'))
user_permission = Permission(UserNeed(169))

