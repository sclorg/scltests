import os

CONFIG_DIR = os.path.abspath('./scltests/configs/MOCK')
RESULT_DIR = os.path.abspath('./scltests/RPMS')
YAML_DIR = os.path.abspath('./scltests/configs/YAML')
SRPMS_DIR = os.path.abspath('./scltests/SRPMS')

REPO = """
[{name}]
name={name}
baseurl=file://{dir}
enabled=1
"""
MACROS = ['_scl_prefix', '_bindir', '_scl_root', '_mandir', '_initddir']


_scl_prefix = '/opt/rh'
_scl_root = '/opt/rh/{scl}/root'
_bindir = '/usr/bin'
_mandir = '/usr/share/man'
_initddir = '/etc/rc.d/init.d'

LOGS = ['build.log', 'root.log', 'state.log']

MOCK_CFG_FILES = ['logging.ini', 'site-defaults.cfg']


MAN_LNG = ['gv', 'gu', 'scn', 'rom', 'alg', 'ale', 'sco', 'mni', 'gd', 'ga', 'mno', 'osa', 'gn', 'alt', 'gl',
           'mwr', 'es_VE', 'ty', 'tw', 'tt', 'tr', 'ts', 'hu_HU', 'to', 'aus', 'tk', 'th', 'roa', 'tg', 'te',
           'uga', 'mwl', 'de_AT', 'fat', 'qaa-qtz', 'fan', 'wo', 'rm', 'en@quot', 'ast_ES', 'din', 'bla', 'cmc',
           'ml', 'ru_RU', 'zh', 'tem', 'en_CA', 'nwc', 'za', 'nl_NL', 'cau', 'zu', 'ter', 'tet', 'mnc', 'kut',
           'es_CO', 'es_CL', 'es_CR', 'kum', 'sus', 'new', 'sux', 'ms', 'men', 'mul', 'lez', 'eka', 'akk', 'dra',
           'sat', 'jrb', 'brx', 'sgn', 'sga', 'apa', 'bra', 'tn', 'chb', 'chg', 'en@shaw', 'chk', 'chm', 'chn',
           'cho', 'chp', 'chr', 'sl_SI', 'chy', 'ti', 'vot', 'uk_UA', 'mg', 'be@latin', 'iba', 'mo', 'mn', 'mi',
           'mh', 'mk', 'mt', 'cai', 'del', 'den', 'mr', 'af_ZA', 'ta', 'my', 'cad', 'srn', 'raj', 'el_GR',
           'tai', 'es_GT', 'afh', 'sit', 'enm', 'en_AU', 'nyn', 'nyo', 'gez', 'sio', 'es_UY', 'map', 'mas',
           'lah', 'nym', 'lad', 'fy', 'snk', 'fa', 'mad', 'mag', 'mai', 'fi', 'fj', 'da', 'fo', 'egy', 'fa_IR',
           'znd', 'ss', 'sr', 'sq', 'sw', 'sv', 'su', 'st', 'sk', 'si', 'so', 'sn', 'sm', 'sl', 'sc', 'sa', 'sg',
           'se', 'sd', 'zen', 'kbd', 'afa', 'csb', 'zh_CN.GB2312', 'lg', 'lb', 'fiu', 'ln', 'lo', 'li', 'byn',
           'lt', 'lu', 'fil', 'yi', 'non', 'ceb', 'yo', 'cel', 'bat', 'dak', 'fr', 'dar', 'qu', 'day', 'ssa', 'pam',
           'kpe', 'el', 'eo', 'en', 'es_PR', 'lam', 'ee', 'tpi', 'mdf', 'et_EE', 'sr_RS', 'es_PE', 'lv_LV', 'es_PA',
           'mdr', 'et', 'es', 'ru', 'gon', 'goh', 'sms', 'smn', 'smj', 'hr_HR', 'got', 'rn', 'ro', 'dsb', 'sma',
           'gor', 'nds@NFE', 'ast', 'sr@latin', 'wal', 'sq_AL', 'crh', 'ms_MY', 'ath', 'nb_NO', 'nia', 'xh', 'ff',
           'mak', 'zap', 'kok', 'zxx', 'kos', 'man', 'tog', 'hup', 'am_ET', 'bej', 'bem', 'tsi', 'he_IL', 'ber',
           'nzi', 'sai', 'ang', 'pra', 'bho', 'sal', 'pro', 'it_IT', 'ks@devanagari', 'sad', 'anp', 'rap', 'sas',
           'nqo', 'car', 'min', 'mic', 'efi', 'arn', 'ypk', 'mis', 'kac', 'kab', 'kaa', 'ur_PK', 'kam', 'kar',
           'uz@cyrillic', 'kaw', 'fr_CH', 'tyv', 'fr_CA', 'ka', 'doi', 'kg', 'kk', 'kj', 'ki', 'ko', 'kn', 'km',
           'kl', 'ks', 'kr', 'kw', 'kv', 'ku', 'ky', 'sr@ijekavian', 'suk', 'tkl', 'bua', 'es_AR', 'udm', 'mga',
           'zh_HK', 'hit', 'dyu', 'de', 'cs_CZ', 'dz', 'lui', 'dv', 'hil', 'him', 'gem', 'crp', 'myn', 'bas',
           'gba', 'zh_CN', 'bad', 'ban', 'bal', 'shn', 'bai', 'arp', 'art', 'fr_FR', 'arw', 'fi_FI', 'arc',
           'en_US', 'sem', 'sel', 'nub', 'btk', 'lus', 'mus', 'lua', 'iro', 'ira', 'mun', 'lun', 'luo', 'wa',
           'tup', 'jv', 'zbl', 'tut', 'tum', 'sr@Latn', 'ja', 'cop', 'ilo', 'la', 'gwi', 'pl', 'und', 'tli',
           'tlh', 'ca_ES@valencian', 'ch', 'co', 'ca', 'nds_DE', 'ce', 'pon', 'en_NZ', 'cy', 'sah', 'cs', 'cr',
           'bnt', 'cv', 'cu', 'lv', 'dum', 'pt', 'dua', 'es_EC', 'fro', 'yap', 'frm', 'tiv', 'frs', 'ja_JP',
           'yao', 'pa', 'xal', 'es_ES', 'pi', 'en@boldquot', 'bg_BG', 'es_SV', 'gay', 'oto', 'ota', 'zh_TW',
           'hmn', 'myv', 'gaa', 'fur', 'khi', 'smi', 'it_CH', 'ain', 'rar', 'sla', 'uz@Latn', 've', 'vi', 'is',
           'av', 'iu', 'it', 'vo', 'ii', 'ik', 'io', 'ine', 'ia', 'jpr', 'ie', 'id', 'ig', 'pap', 'es_HN', 'ewo',
           'pau', 'zgh', 'paa', 'pag', 'bn_IN', 'pal', 'gl_ES', 'syc', 'phi', 'nog', 'phn', 'nic', 'ko_KR', 'dgr',
           'syr', 'niu', 'gsw', 'jbo', 'nb', 'es_NI', 'nl_BE', 'ca@valencia', 'sam', 'hai', 'gmh', 'cus', 'wen',
           'ady', 'elx', 'ada', 'pt_PT', 'haw', 'bin', 'bik', 'pt_BR', 'mos', 'moh', 'tig', 'eu_ES', 'tvl', 'sv_SE',
           'ijo', 'kmb', 'peo', 'tl', 'umb', 'tmh', 'fon', 'zh_TW.Big5', 'hsb', 'be', 'bg', 'ba', 'ps', 'bm', 'bn',
           'bo', 'bh', 'bi', 'br', 'bs', 'rup', 'zza', 'om', 'oj', 'ace', 'ach', 'oc', 'kru', 'srr', 'kro', 'krl',
           'krc', 'nds', 'os', 'or', 'sog', 'nso', 'az_IR', 'son', 'fr_BE', 'de_CH', 'vai', 'wak', 'ca_ES', 'frr',
           'lol', 'mkh', 'awa', 'loz', 'gil', 'was', 'war', 'hz', 'hy', 'sid', 'hr', 'ht', 'hu', 'hi', 'ho', 'ha',
           'bug', 'he', 'uz', 'default', 'ur', 'en_GB', 'uk', 'ug', 'aa', 'ab', 'ae', 'af', 'ak', 'am', 'an', 'eu',
           'as', 'ar', 'inh', 'my_MM', 'kho', 'ay', 'kha', 'az', 'inc', 'nl', 'nn', 'no', 'na', 'nah', 'nai', 'nd',
           'ne', 'ng', 'ny', 'nap', 'grb', 'grc', 'nr', 'sr@ije', 'nv', 'zun', 'rw', 'de_DE', 'es_MX',
           'sr@ijekavianlatin', 'es_DO', 'cpe', 'cpf', 'cpp', 'pl_PL']

IMP_FLDS = ['/etc/scl/prefixes/{0}',
            '/opt/rh/{0}',
            '/opt/rh/{0}/enable',
            '/opt/rh/{0}/root',
            '/opt/rh/{0}/root/bin',
            '/opt/rh/{0}/root/boot',
            '/opt/rh/{0}/root/dev',
            '/opt/rh/{0}/root/etc',
            '/opt/rh/{0}/root/home',
            '/opt/rh/{0}/root/lib',
            '/opt/rh/{0}/root/lib64',
            '/opt/rh/{0}/root/media',
            '/opt/rh/{0}/root/mnt',
            '/opt/rh/{0}/root/opt',
            '/opt/rh/{0}/root/proc',
            '/opt/rh/{0}/root/root',
            '/opt/rh/{0}/root/run',
            '/opt/rh/{0}/root/run/lock',
            '/opt/rh/{0}/root/sbin',
            '/opt/rh/{0}/root/srv',
            '/opt/rh/{0}/root/sys',
            '/opt/rh/{0}/root/tmp',
            '/opt/rh/{0}/root/usr', ]
