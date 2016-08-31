import sublime, sublime_plugin, re

settings_file_name = 'Frontal.sublime-settings'
# see https://forum.sublimetext.com/t/dev-build-3118/21270
class Frontal(sublime_plugin.ViewEventListener):
    def __init__(self, view):
        self.view = view
        self.phantom_set = sublime.PhantomSet(view)
        self.timeout_scheduled = False
        self.needs_update = False
        settings = sublime.load_settings(settings_file_name)
        self.enabled = settings.get('enabled')
        # print (self.enabled)
        if settings.get('enabled') == False:
            self.phantom_set.update([])
            print ('not enabled')
            return
        PHANTOM_SUPPORT = int(sublime.version()) >= 3118
        if not PHANTOM_SUPPORT:
            print ('no Phantom support')
            return
        self.update_phantoms()

    @classmethod
    def is_applicable(cls, settings):
        syntax = settings.get('syntax')
        print (syntax)
        mde = 'Packages/MarkdownEditing/Markdown.tmLanguage'
        pt = 'Packages/Text/Plain text.tmLanguage'
        md = 'Packages/Markdown/Markdown.sublime-syntax'
        mmd = 'Packages/Markdown/MultiMarkdown.sublime-syntax'
        return syntax == mde or syntax == pt or syntax == md or syntax == mmd and self.enabled == True and PHANTOM_SUPPORT == True

    def update_phantoms(self):
        phantoms = []
        lines = self.view.find_all('^---')

        counter = 2
        for r in lines:
            # line_region = self.view.line(r.a)
            # line = self.view.substr(line_region)
            name = '<div style="background-color:rgba(123,123,123,0.4);">Frontal Slide: ' + str(counter) + '</div>'
            # sublime.LAYOUT_BELOW
            # sublime.LAYOUT_BLOCK
            # https://www.sublimetext.com/docs/3/api_reference.html#sublime.Phantom
            phantoms.append(sublime.Phantom(
            r,
            name,
            sublime.LAYOUT_BELOW))
            counter = counter + 1

        self.phantom_set.update(phantoms)

    def handle_timeout(self):
        self.timeout_scheduled = False
        if self.needs_update:
            self.needs_update = False
            self.update_phantoms()

    def on_modified(self):
        # Call update_phantoms(), but not any more than 10 times a second
        if self.timeout_scheduled:
            self.needs_update = True
        else:
            sublime.set_timeout(lambda: self.handle_timeout(), 100)
            self.update_phantoms()

# class FrontalToggleCommand(sublime_plugin.TextCommand):
#     def run(self, edit):
#         print('toggle')
#         settings = sublime.load_settings(settings_file_name)
#         print(settings)
#         if settings.enabled == True:
#             settings.enabled = False
#         else:
#             settings.enabled = True
#         sublime.save_settings(settings_file_name)



