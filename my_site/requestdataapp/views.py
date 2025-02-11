from typing import Dict

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from .forms import UploadFileForm, UserBioForm


def process_get_view(request: HttpRequest) -> HttpResponse:
    line_a: str = request.GET.get("a", "")
    line_b: str = request.GET.get("b", "")
    result: str = line_a + line_b
    context: Dict[str, str] = {"line_a": line_a, "line_b": line_b, "result": result}

    return render(request, "requestdataapp/request-query-params.html", context)


def user_form(request: HttpRequest) -> HttpResponse:
    context = {"form": UserBioForm()}
    return render(
        request=request,
        template_name="requestdataapp/user-bio-form.html",
        context=context,
        status=201,
    )


def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form: UploadFileForm = UploadFileForm(request.POST, request.FILES)
        http_status_code: int = 201
        if form.is_valid():
            # file: HttpRequest = request.FILES["myfile"]
            file = form.cleaned_data["myfile"]

            if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
                raise ValidationError(message="File size is more than 1mb")

            fs: FileSystemStorage = FileSystemStorage(location="requestdataapp/media")
            filename: str = fs.save(file.name, file)
            print("Saved file", filename)

    else:
        form = UploadFileForm()
        http_status_code = 200

    context: Dict[str, UploadFileForm] = {"form": form}

    return render(
        request=request,
        template_name="requestdataapp/file-upload.html",
        context=context,
        status=http_status_code,
    )
