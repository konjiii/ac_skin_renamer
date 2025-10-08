from html.parser import HTMLParser

html_str = '<option value="2557">benwood_racing_14</option><option value="2558">benwood_racing_15</option><option value="2559">detroit_motorsports_04</option><option value="2560">detroit_motorsports_34</option><option value="2561">enstone_racing_42</option><option value="2562">enstone_racing_61</option><option value="2563">fortix_vrc_racing_08</option><option value="2564">fortix_vrc_racing_96</option><option value="2565">milloms_fa_18</option><option value="2566">milloms_fa_24</option><option value="2567">panther_racing_05</option><option value="2568">panther_racing_06</option><option value="2569">revision_racing_17</option><option value="2570">revision_racing_45</option><option value="2571">vrc_motorsport_07</option><option value="2572">vrc_motorsport_29</option>'


class RorHTMLParser(HTMLParser):
    def __init__(self):
        super().__init__()

        self.ror_skins = list()

    def handle_starttag(self, _tag, _attrs):
        pass

    def handle_data(self, data):
        self.ror_skins.append(data)

    def handle_endtag(self, _tag):
        pass
