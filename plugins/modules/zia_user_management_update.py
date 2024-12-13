#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2023 Zscaler Inc, <devrel@zscaler.com>

#                             MIT License
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = r"""
---
module: zia_user_management_update
short_description: "Updates a user"
description:
  - "Updates a user"
author:
  - Basil Wallace (@tarmael)
version_added: "1.4.0"
requirements:
    - Zscaler SDK Python can be obtained from PyPI U(https://pypi.org/project/zscaler-sdk-python/)
notes:
    - Check mode is not supported.
extends_documentation_fragment:
  - zscaler.ziacloud.fragments.provider
  - zscaler.ziacloud.fragments.documentation

options:
  id:
    description: "User ID."
    required: false
    type: int
  name:
    description: "User name. This appears when choosing users for policies."
    required: false
    type: str
  email:
    description: "Doc string is temporary."
    required: false
    type: str
  admin:
    description: "Doc string is temporary."
    required: false
    type: str
  groups:
    description: "Doc string is temporary."
    required: false
    type: str
  comments:
    description: "Doc string is temporary."
    required: false
    type: str
  department:
    description: "Doc string is temporary."
    required: false
    type: str
"""

EXAMPLES = r"""
- name: Gets a list of a single user
  zscaler.ziacloud.zia_user_management_update:
    provider: '{{ provider }}'
    name: "Adam Ashcroft"
    id: 45677777
    
"""

RETURN = r"""
results:
  description: List of users modified by the module.
  returned: always
  type: list
  elements: dict
  contains:
    id:
      description: The unique identifier for the user.
      type: int
      sample: 45513075
    name:
      description: The name of the user.
      type: str
      sample: "Adam Ashcroft"
    email:
      description: The email address of the user.
      type: str
      sample: "adam.ashcroft@bd-hashicorp.com"
    admin_user:
      description: Flag indicating if the user has admin privileges.
      type: bool
      sample: false
    is_non_editable:
      description: Flag indicating if the user's profile is non-editable.
      type: bool
      sample: false
    deleted:
      description: Flag indicating if the user's profile has been deleted.
      type: bool
      sample: false
    department:
      description: The department to which the user belongs.
      type: dict
      contains:
        id:
          description: The unique identifier of the department.
          type: int
          sample: 45513014
        name:
          description: The name of the department.
          type: str
          sample: "Engineering"
    groups:
      description: List of groups to which the user belongs.
      type: list
      elements: str
      sample: []
  sample: [
    {
      "admin_user": false,
      "deleted": false,
      "department": {
        "id": 45513014,
        "name": "Engineering"
      },
      "email": "adam.ashcroft@bd-hashicorp.com",
      "groups": [],
      "id": 45513075,
      "is_non_editable": false,
      "name": "Adam Ashcroft"
    }
  ]
"""

from traceback import format_exc

from ansible.module_utils._text import to_native
from ansible.module_utils.basic import AnsibleModule
from ansible_collections.zscaler.ziacloud.plugins.module_utils.zia_client import (
    ZIAClientHelper,
)


def core(module):
    user_id = module.params.get("id", None)
    user_name = module.params.get("name", None)
    user_email = module.params.get("email", None)
    user_admin = module.params.get("admin", None)
    user_groups = module.params.get("groups", None)
    user_comments = module.params.get("comments", None)
    user_department = module.params.get("department", None)
    user_kwargs = dict(
      name = user_name,
      email = user_email,
      adminUser = user_admin,
      groups = user_groups,
      comments = user_comments,
      department = user_department
    )
    filter_kwargs = {key:value for key,value in user_kwargs.items() if value is not None}

    client = ZIAClientHelper(module)
    user_results = client.users.update_user(user_id, **filter_kwargs).to_dict()
    module.exit_json(changed=False, results=user_results)


def main():
    argument_spec = ZIAClientHelper.zia_argument_spec()
    argument_spec.update(
        id=dict(type="int", required=True),
        name=dict(type="str", required=False),
        email=dict(type="str", required=False),
        admin=dict(type="bool", required=False),
        groups=dict(type="dict", required=False),
        comments=dict(type="str", required=False),
        department=dict(type="dict", required=False),
    )
    module = AnsibleModule(argument_spec=argument_spec, supports_check_mode=True)
    try:
        core(module)
    except Exception as e:
        module.fail_json(msg=to_native(e), exception=format_exc())


if __name__ == "__main__":
    main()
