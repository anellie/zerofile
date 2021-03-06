from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseGone, Http404
from django.template import loader
from zerofile.models import File
from zerofile.settings import FILEDIR

def download(request, file_id):
    """ Serve file corresponding to the id """
    dbfile = get_object_or_404(File, _id=file_id)
    if dbfile.deleted:
        template = loader.get_template('downloader/deleted.html')
        return HttpResponseGone(template.render({'fileid': dbfile._id}, request=request))

    try:
        with open(FILEDIR + dbfile._id, "rb") as i:
            response = HttpResponse(i.read(), content_type=dbfile.mime)
            response['Content-Disposition'] = 'inline; filename=%s' % dbfile.name
            return response
    except:
        raise Http404("File not found")