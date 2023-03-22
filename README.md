# Atividade Ecommerce
## Frameworks para Desenvolvimento de Software


Para que seja possível inicializar o flask tanto no *(cmd/powershell/terminal)* 

No Linux.

```
export FLASK_APP=leb
flask run
```
:rocket: No Windows. :rocket:

```
set FLASK_APP=leb
python -m flask run

# Ou somente #

flask run
```


### Caso queira fazer um ambiente virtual, siga os passos a seguir:

Instalando o Virtual Environment
```
python3 -m pip install virtualenv
```
⋘ ──── ∗ ⋅◈⋅ ∗ ──── ⋙

Então faça uma nova pasta


**OBS:** digite sem aspas

```
mkdir "nome que desejar"
cd "nome que desejar"
```

Ou continue utilizando a pasta **L&B Vendas**


⋘ ──── ∗ ⋅◈⋅ ∗ ──── ⋙

Crie o ambiente virtual

```
python3 -m venv testenv ou "nome que desejar"
```
⋘ ──── ∗ ⋅◈⋅ ∗ ──── ⋙

Ativando o ambiente virtual no **Linux**

```
source testenv/bin/activate
```
Ativando o ambiente virtual no **Windows**

PowerShell

```
.\testenv\Scripts\activate.ps1
```

CMD
```
.\testenv\Scripts\activate.bat
```
