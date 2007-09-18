from HTMLParser import HTMLParser
import os
import sys
import urllib
import urlparse

#------ global variable

# base url
basepla = 'nzmath.sourceforge.net'
basewiki = '/wiki/'
basedoc = '/doc/'
HPpla = 'tnt.math.metro-u.ac.jp'
HPdoc = '/nzmath/'

# normal option
ad_list = set(['UserManual'])
p_out = True
sleeptime = 1

#------ utility function
def back_to_tag(tag, attrs):
    str = '<' + tag
    for (prop, val) in attrs:
         str += ' ' + prop + '="' + val + '"'
    str += '>'
    return str

def getHeader(files):
    str = '<div id="header">' + '\n'
    str += ' <h1 class="title">'
    str += '<a href="'
    str += convertDocURL(files)
    str += '">?' + urllib.unquote(files) + '</a></h1>' + '\n'
    str += '</div>' + '\n'
    return str

def getFooter():
    str = '<div id="footer">' + '\n'
    str += ' Copyright &copy; 2003-2007,'
    str += '<a href="'
    str += convertHPURL('')
    str += '">' + 'NZMATH</a> deveropment group' + '\n'
    str += '</div>' + '\n'
    return str

def convertFileName(url):
    split_url = urlparse.urlparse(url)
    if split_url[1] == basepla:
        if split_url[4] == 'UserManual':
            sol = "index.html"
        elif split_url[4] == 'Install':
            sol = "install.html"
        elif split_url[4] == 'Tutorial':
            sol = "tutorial.html"
        elif split_url[4] in ('BracketName', 'InterWikiName', 'References'):
            return url
        elif split_url[4][:8] == 'cmd=edit':
            return url
        else: # modules
            sol = str(split_url[4])
            sol = sol.replace('.py', '').replace('%2F', '_').replace('%20%28ja%29', '.ja')
            sol = 'modules/' + sol + '.html'
        return (sol, split_url[5], split_url[4])
    else:
        return url

def convertWikiURL(files):
    return urlparse.urlunsplit( ('http', basepla, basewiki, files, '') )

def convertDocURL(files):
    return urlparse.urlunsplit( ('http', basepla, basedoc, files, '') )

def convertHPURL(files):
    return urlparse.urlunsplit( ('http', HPpla, HPdoc + files, '', '') )

#------ Error Class
class NoneOutput(Exception):
    pass

class InputError(Exception):
    pass

#------ create modified html
class MyWikiParser(HTMLParser):
    def __init__(self, files):
        self.files = files
        self.url = convertDocURL(files)
        conv = convertFileName(self.url)[0]
        if conv.find('modules/') == -1:
            self.up = True
        else:
            self.up = False
        self.f = file(conv, 'w')
        if p_out:
            print "make from " + self.url
        self.deal = False
        HTMLParser.__init__(self)

    def handle_data(self, data):
        if not(self.deal):
            p_data = data.replace('NZMATHWiki', 'NZMATH')
            self.f.write(p_data)

    def handle_starttag(self, tag, attrs):
        if not(self.deal):
            try:
                p_attrs = attrs
                if tag == 'div':
                    if attrs:
                        if attrs[0][0] == 'id':
                            if attrs[0][1] == 'footer':
                                self.deal = 'div'
                                self.f.write(getFooter())
                                raise NoneOutput
                            if attrs[0][1] == 'header':
                                self.deal = 'div'
                                self.f.write(getHeader(self.files))
                                raise NoneOutput
                            if attrs[0][1] == 'lastmodified':
                                self.deal = 'div'
                                raise NoneOutput
                        if attrs[0][0] == 'class':
                            if attrs[0][1] == 'jumpmenu':
                                self.deal = 'div'
                                raise NoneOutput
                if tag == 'a':
                    if attrs[0][0] == 'href':
                        f_name = convertFileName(attrs[0][1])
                        if isinstance(f_name, tuple):
                            p_f_name = f_name[0]
                            if not(self.up):
                                if p_f_name.find('modules/') == -1:
                                    p_f_name = '../' + p_f_name
                                else:
                                    p_f_name = p_f_name[8:]
                            if f_name[1] != '':
                                p_attrs[0] = (attrs[0][0], p_f_name + '#' + f_name[1])
                            else:
                                p_attrs[0] = (attrs[0][0], p_f_name)
                            if not(os.path.exists(f_name[0])):
                                ad_list.add(f_name[2])
                    if attrs[0][0] == 'class':
                        if attrs[0][1] == 'anchor_super':
                            del p_attrs[3]
                            del p_attrs[2]
                self.f.write(back_to_tag(tag, p_attrs))
            except NoneOutput:
                pass

    def handle_endtag(self, tag):
        if not(self.deal):
            self.f.write('</' + tag + '>')
        if self.deal == tag:
            self.deal = False

    def handle_startendtag(self, tag, attrs):
        if not(self.deal):
            try:
                p_attrs = list(attrs)
                if tag == 'link':
                    if attrs[0][0] == 'rel':
                        if attrs[1][0] == 'href':
                            if self.up:
                                p_attrs[1] = (attrs[1][0], 'default.css')
                            else:
                                p_attrs[1] = (attrs[1][0], '../default.css')
                if tag == 'img':
                    raise NoneOutput
                self.f.write(back_to_tag(tag, p_attrs)[:-1] + ' />')
            except NoneOutput:
                pass

    def handle_charref(self, ref):
        if not(self.deal):
            self.f.write('&#' + ref + ';')

    def handle_entityref(self, name):
        if not(self.deal):
            self.f.write('&' + name + ';')

    def handle_comment(self, data):
        if not(self.deal):
            self.f.write('<!--' + data + '-->')

    def handle_decl(self, decl):
        if not(self.deal):
            self.f.write('<!' + decl + '>')

    def handle_pi(self, data):
        if not(self.deal):
            self.f.write('<?' + data + '>')

    def close(self):
        self.f.close()
        HTMLParser.close(self)

    def feeds(self):
        HTMLParser.feed(self, urllib.urlopen(self.url).read())

#------ preparation
def main(basepath):
    current = os.getcwd()
    try:
        if not(os.path.exists(basepath)):
            ans = 'y'
            if p_out:
                print "Do you want to create " + basepath + "?(y/n)"
                ans = sys.stdin.read(1)
                print ""
            if ans in ('y', 'Y'):
                pass
            elif ans in ('n', 'N'):
                raise NoneOutput
            else:
                raise InputError
        else:
            m_path = os.path.join(basepath, 'nzmath/manual')
            if os.path.exists(m_path):
                ans = 'y'
                if p_out:
                    print "Do you want to remove " + m_path + "?(y/n)"
                    ans = sys.stdin.read(1)
                    print ""
                if ans in ('y', 'Y'):
                    for root, dirs, files in os.walk(m_path, topdown=False):
                        for name in files:
                            os.remove(os.path.join(root, name))
                        for name in dirs:
                            os.rmdir(os.path.join(root, name))
                elif ans in ('n', 'N'):
                    raise NoneOutput
                else:
                    raise InputError
        dirname = os.path.join(basepath, 'nzmath/manual/modules')
        os.makedirs(dirname)
        os.chdir(os.path.join(basepath, 'nzmath/manual/'))
        urllib.urlretrieve(convertHPURL('manual/default.css'), 'default.css')
        while ad_list:
            files = ad_list.pop()
            os.system('sleep ' +  str(sleeptime))
            MyWikiParser(files).feeds()
        if p_out:
            print "\n" + "All process is done!" + "\n"
            print "Ok, now created nzmath-current manual located to"
            print os.path.join(basepath, "nzmath")
            print "if you check difference between nzmath-cvs manual, with GNU diff,"
            print "$ diff -ubBr /tmp/nzmath/manual {your-nzmathcvs-repo}/manual"
            print "or you check only new version files,"
            print "$ diff -r --brief /tmp/nzmath/manual {your-nzmathcvs-repo}/manual ."
    except NoneOutput:
        if p_out:
            print 'end.'
    except InputError:
        raise ValueError, "Invalid input!"
    except:
        if p_out:
            print "Check" + basepath + "(dir? truly path? and so on.)\n"
        print sys.exc_info()[0]
        raise
    finally:
        os.chdir(current)

#------ start!
if __name__ == '__main__':
    basepath = './tmp'
    if len( sys.argv) > 1:
        basepath = sys.argv[1]

    main(basepath)