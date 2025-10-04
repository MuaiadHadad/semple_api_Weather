# Use uma imagem Python oficial como base
FROM python:3.9-slim
# Definir o diretório de trabalho
WORKDIR /app
# Copiar ficheiros de dependências
COPY requirements.txt .
# Instalar dependências
RUN pip install --no-cache-dir -r requirements.txt
# Copiar o código da aplicação
COPY . .
# Expor a porta da aplicação
EXPOSE 5000
# Definir variáveis de ambiente
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV PORT=5000
# Comando para executar a aplicação
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
