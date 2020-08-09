import setuptools,platform,os
if platform.system().startswith("CYGWIN") and platform.machine()=="x86_64":
  pass
else:
  raise OSError("chapas-cygwin64 only for 64-bit Cygwin")

CHAPAS_URL="https://drive.google.com/uc?export=download&id=0BwG_CvJHq43fNDlqSkVSREkzaEk"
JDK_URL="https://github.com/ojdkbuild/ojdkbuild/releases/download/java-1.8.0-openjdk-1.8.0.252-2.b09/java-1.8.0-openjdk-jre-1.8.0.252-2.b09.ojdkbuild.windows.x86_64.zip"

if not os.path.isdir("local/chapas"):
  import urllib.request,tarfile,zipfile,glob,subprocess
  from http.cookiejar import CookieJar
  p=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
  r=p.open(CHAPAS_URL)
  c=""
  for i,j in r.getheaders():
    if i=="Set-Cookie" and j.startswith("download_warning_"):
      try:
        k=j.index("=")
        c="&confirm="+j[k+1:j.index(";",k)]
      except:
        pass
  r.close()
  r=p.open(CHAPAS_URL+c)
  with open("chapas.tar.gz","wb") as f:
    f.write(r.read())
  r.close()
  with tarfile.open("chapas.tar.gz") as z:
    z.extractall("local")
  os.renames(glob.glob("local/chapas-*")[0],"local/chapas")
  f,h=urllib.request.urlretrieve(JDK_URL)
  with zipfile.ZipFile(f) as z:
    z.extractall("local")
  os.renames(glob.glob("local/java-*")[0],"local/chapas/jdk")
  for f in glob.glob("local/chapas/jdk/bin/**/*.[ed][xl][el]",recursive=True):
    os.chmod(f,0o755)

setuptools.setup(
  name="chapas-cygwin64",
  version="0.4.3",
  packages=setuptools.find_packages(),
  data_files=[(p,[os.path.join(p,e) for e in f]) for p,d,f in os.walk("local") if f!=[]],
  install_requires=["cabocha-cygwin64@git+https://github.com/KoichiYasuoka/cabocha-cygwin64"]
)
