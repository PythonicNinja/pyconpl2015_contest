import md5

original = 'melosba'
reverse = original[::-1]

print original
print reverse

print "".join(map(unicode, map(ord, original)))
print "".join(map(unicode, map(ord, reverse)))

print md5.md5(original).hexdigest()
print md5.md5(reverse).hexdigest()


print md5.md5(original).hexdigest()[::-1]
print md5.md5(reverse).hexdigest()[::-1]
