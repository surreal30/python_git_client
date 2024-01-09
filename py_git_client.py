import os
import hashlib
import zlib

def init(repo):
	os.mkdir(repo)
	os.mkdir(os.path.join(repo, '.git'))
	for name in ['objects', 'refs', 'refs/heads']:
		os.mkdir(os.path.join(repo, '.git', name))
	write_file(os.path.join(repo, '.git', 'HEAD'), b'ref: refs/heads/master')
	print("Initialised empty repository: {}".format(repo))

def hash_object(data, obj_type, write = True):
	"""Compute hash of object data of given type and write to object store if "write" is true.
	Return SHA1 object as hex string"""
	header = '{} {}'.format(obj_type, len(data)).encode()
	full_data = header + b'\x00' + data
	sha1 = hashlib.sha1(full_data).hexdigest()
	
	if write:
		path = os.path.join('.git', 'objects', sha1[:2], sha1[2:])
		if not os.path.exists(path):
			os.makedirs(os.path.dirname(path), exist_ok = True)
			write_file(path, zlib.compress(full_data))

	return sha1
