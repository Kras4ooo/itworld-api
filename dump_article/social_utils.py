import json
import urllib2

class SocialUtils(object):

    def counter_likes(self, link):
        """
        Get Facebook and Google+ counter likes
        
        likes - FB
        shares - FB or TW
        comments - FB or TW or G+
        tweets - TW
        plusones - G+
        """
        response = urllib2.build_opener().open(self.create_link(link)).read()
        common_likes = self.counter_parse(response)
        return common_likes
    
    def counter_parse(self, response):
        """
        Parse JSON and get link count
        """
        return json.loads(response)
        
    
    def create_link(self, link):
        """ 
        Create encode link
        """ 
        original_link = "http://social-count.eu01.aws.af.cm/%s" % link
        return original_link