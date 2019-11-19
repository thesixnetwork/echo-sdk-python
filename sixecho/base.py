class Base(object):
    def __init__(self):
        self.comment_info = {}
        self.ref_info = {}

    def set_common_info(self, common_info):
        """
          common_info: Required
           - title Required title show sixecho work
           - image_url Option image show sixecho work
           - parent_id Option parent id show reference in sixecho work
           - tags Option tag show sixecho work

        """
        self.common_info = common_info

    def set_ref_info(self, ref_info):
        """
        ref_info: Required
         - ref_owner Required string
         - owner Required string
         - ref_creator string
         - creator  Required string
        """
        self.ref_info = ref_info
