# Copyright 2016 EMC Corporation
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from cinder.api.v2.views import volumes as views_v2


class ViewBuilder(views_v2.ViewBuilder):
    """Model a volumes API V3 response as a python dictionary."""

    def quick_summary(self, volume_count, volume_size):
        """Number of volumes and size of volumes."""
        return {
            'volume-summary': {
                'total_count': volume_count,
                'total_size': volume_size
            },
        }

    def detail(self, request, volume):
        """Detailed view of a single volume."""
        volume_ref = super(ViewBuilder, self).detail(request, volume)

        req_version = request.api_version_request
        # Add group_id if min version is greater than or equal to 3.13.
        if req_version.matches("3.13", None):
            volume_ref['volume']['group_id'] = volume.get('group_id')

        # Add provider_id if min version is greater than or equal to 3.21
        # for admin.
        if (request.environ['cinder.context'].is_admin and
                req_version.matches("3.21", None)):
            volume_ref['volume']['provider_id'] = volume.get('provider_id')

        return volume_ref

    def diskusage_list(self, request, volumes, volume_count=None):
        """Show a list of volumes, along with their disk usage info."""
        return self._list_view(self.diskusage, request, volumes,
                               volume_count)

    def diskusage(self, request, volume):
        return {
            'volume': {
                'id': volume['id'],
                'name': volume['display_name'],
                'links': self._get_links(request, volume['id']),
                # We just hardcode 10 here for a test, replace it with
                # code that calculates the disk usage
                'disk_usage': '10',
            },
        }
