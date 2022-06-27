<p align="center">
  <img width="500" height="140" alt="CacheLib" src="https://www.inovachaves.com.br/img/Logo.png">
</p>

# Sysred

Sistema desenvolvido por Inova Chaves para gestão empresarial

## Virtual Enviroment

Criação do ambiente virtual no Windows

```sh
cd C:\Personal\Dropbox\Develop\sysred\backend
py -3 -m venv .venv
.venv\scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Database Configuration

Criação da estrutura de tabelas do banco de dados

```cmd
cd C:\Personal\Dropbox\Develop\sysred\backend
py -3 -m venv .venv
.venv\scripts\activate
```
```python
>>> from app import db
>>> db.create_all()
```

## Steps to Install

A aplicação está rodando no servidor icssrvapp01(159.65.65.132)

```sh
cd /opt/
git clone git@github.com:giulianopedrotti/sysred.git
cd sysred/
scl enable rh-python38 bash
python -m venv .venv
cd ..
chown admininova:nginx -R sysred/
cd sysred/
```
```python
source .venv/bin/activate
pip install --upgrade pip
```
```sh
cp sysred.service /etc/systemd/system/sysred.service
cat /etc/systemd/system/sysred.service
systemctl start sysred
systemctl enable sysred
systemctl status sysred
cp sysred.conf /etc/nginx/conf.d/
certbot --nginx -d sysred.inovachaves.com.br
```