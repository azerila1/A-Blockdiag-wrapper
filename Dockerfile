FROM python:3.6.4-alpine3.7


ENV http_proxy http://XX:XX@XX.XX.XX:XXXX
ENV https_proxy https://XX:XX@XX.XX.XX:XXXX
RUN apk --no-cache add musl-dev linux-headers g++

RUN apk add --no-cache \
    build-base cairo-dev cairo cairo-tools \
    #pillow dependencies
    jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev 

RUN pip3 install --upgrade pip
RUN pip3 install "flask==1.0.1"
RUN pip3 install "setuptools==39.2.0" "CairoSVG==2.1.3"
RUN pip3 install "pandas==0.23.4" "blockdiag" "pillow"

RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/box.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/beginpoint.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/base.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/actor.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/circle.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/ellipse.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/square.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/roundedbox.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/minidiamond.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/diamond.py
RUN sed -i.bak "s/if kwargs.get('shadow')/if False:#/g" /usr/local/lib/python3.6/site-packages/blockdiag/noderenderer/cloud.py

COPY . .


CMD python3 /group_diag.py
