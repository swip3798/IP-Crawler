# -*- mode: python -*-

block_cipher = None


a = Analysis(['C:\\Users\\d070527\\Documents\\Private\\Programming\\Python\\IP Crawler\\IP-Crawler\\pingcrawler.py'],
             pathex=['C:\\Users\\d070527\\Documents\\Private\\Programming\\Python\\IP Crawler\\IP-Crawler'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='pingcrawler',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='pingcrawler')
