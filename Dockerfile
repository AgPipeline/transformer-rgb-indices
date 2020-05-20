# automatically generated: 2020-05-20T08:40:04.406489
FROM agpipeline/rgb-plot-base-image:latest
LABEL maintainer="Unknown <Unknown@gmail.com>"

COPY requirements.txt packages.txt /home/extractor/

USER root

RUN [ -s /home/extractor/packages.txt ] && \
    (echo "Installing packages" && \
        apt-get update && \
       cat /home/extractor/packages.txt | xargs apt-get install -y --no-install-recommends && \
        rm /home/extractor/packages.txt && \
        apt-get autoremove -y && \
        apt-get clean && \
        rm -rf /var/lib/apt/lists/*) || \
    (echo "No packages to install" && \
        rm /home/extractor/packages.txt)

RUN [ -s /home/extractor/requirements.txt ] && \
    (echo "Install python modules" && \
    python -m pip install -U --no-cache-dir pip && \
    python -m pip install --no-cache-dir setuptools && \
     python -m pip install --no-cache-dir -r /home/extractor/requirements.txt && \
     rm /home/extractor/requirements.txt) || \
    (echo "No python modules to install" && \
     rm /home/extractor/requirements.txt)

USER extractor

COPY algorithm_rgb.py /home/extractor/
