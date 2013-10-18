# -*- coding:utf-8 -*-


class HelperMixin(object):

    """ Helper class to enhance the string and text
        proccess tasks.
    """
    def join(self, group):
        if len(group) > 0:
            return ''.join(group).strip()
        else:
            return ""
