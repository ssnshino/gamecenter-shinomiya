"""Fail-closed check of proposed effective Compose against the active deployment."""
import json, sys, pathlib, stat

def check(config, unity, root, sha):
    assert config['name'] == 'gamecenter-shinomiya'
    services = config['services']
    assert set(services) == {'classic', 'unity-web', 'gateway'}
    assert unity['State']['Running'] is True
    assert services['unity-web']['image'] == unity['Config']['Image']
    for name in services:
        s = services[name]
        assert s['container_name'] == 'gamecenter-shinomiya-' + name
        assert not any(s.get(k) for k in ('privileged','devices','cap_add','network_mode','pid','ipc'))
    classic = services['classic']; gateway = services['gateway']
    assert classic['image'] == 'gamecenter-shinomiya-classic:' + sha
    assert gateway['image'] == 'gamecenter-shinomiya-gateway:' + sha
    assert classic['environment']['GIT_HASH'] == sha
    assert classic['read_only'] is True
    vols = classic['volumes']
    assert len(vols) == 1 and vols[0]['type'] == 'bind'
    assert vols[0]['source'] == root + '/runtime/classic' and vols[0]['target'] == '/data'
    assert not services['unity-web'].get('volumes') and not gateway.get('volumes')
    assert not classic.get('ports') and not services['unity-web'].get('ports')
    ports = gateway['ports']; assert len(ports) == 1
    assert ports[0]['host_ip'] == '127.0.0.1' and str(ports[0]['published']) == '18094' and str(ports[0]['target']) == '80'
    assert set(classic['networks']) == set(services['unity-web']['networks']) == {'internal'}
    assert set(gateway['networks']) == {'internal','wos-proxy-network'}
    assert config['networks']['wos-proxy-network']['external'] is True
    hosts = set(gateway['environment']['VIRTUAL_HOST'].split(','))
    assert hosts == {'unity-games.wos.ktsys.jp','airrace-web.wos.ktsys.jp','rust-sandbox.wos.ktsys.jp'}
    assert str(gateway['environment']['VIRTUAL_PORT']) == '80'

def check_live_classic(classic, root):
    assert classic['State']['Running'] is True
    assert classic['Config']['User'] == '1000:1000'
    mounts=[v for v in classic['Mounts'] if v['Destination']=='/data']
    assert len(mounts)==1
    assert mounts[0]['Type']=='bind' and mounts[0]['Source']==root+'/runtime/classic' and mounts[0]['RW'] is True

def runtime_check(root):
    root=pathlib.Path(root)
    assert not root.is_symlink() and root.is_dir()
    st=root.stat(); assert st.st_uid == 1000 and st.st_mode & stat.S_IWUSR and st.st_mode & stat.S_IXUSR
    for name in ['breakout_scores','dungeon_scores','fighting_scores','truckers_scores','airrace_scores','airrace_ghosts']:
        p=root/(name+'.json'); assert not p.is_symlink() and p.is_file()
        st=p.stat(); assert st.st_uid == 1000 and st.st_mode & stat.S_IRUSR and st.st_mode & stat.S_IWUSR
        value=json.loads(p.read_text()); assert isinstance(value,(list,dict))

if __name__ == '__main__':
    if sys.argv[1] == '--live-classic':
        check_live_classic(json.load(open(sys.argv[2]))[0],sys.argv[3]); sys.exit(0)
    if sys.argv[1] == '--runtime':
        runtime_check(sys.argv[2]); sys.exit(0)
    with open(sys.argv[1]) as f: config=json.load(f)
    with open(sys.argv[2]) as f: unity=json.load(f)[0]
    check(config, unity, sys.argv[3], sys.argv[4])
