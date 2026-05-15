from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import requests

TOKEN = "8705080725:AAEcus-In_8vtTLTSsPczS-Lj_pqyfeDZZE"

# memória simples
memoria = {}

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    mensagem = update.message.text

    # cria memória
    if user_id not in memoria:
        memoria[user_id] = []

    memoria[user_id].append(f"Usuário: {mensagem}")

    # mantém últimas mensagens
    historico = "\n".join(memoria[user_id][-10:])

    prompt = f"""
Você é uma inteligência artificial extremamente avançada, inteligente e natural.

Seu objetivo é conversar como um humano real altamente inteligente.

REGRAS ABSOLUTAS:

- Responda SEMPRE em português brasileiro.
- Nunca responda em inglês.
- Seja extremamente inteligente e útil.
- Fale de forma natural e humana.
- Seja amigável, moderna e carismática.
- Explique tudo de forma clara e fácil.
- Dê respostas completas e bem elaboradas.
- Pense antes de responder.
- Nunca diga que é limitada.
- Nunca diga que não consegue ajudar.
- Nunca fale sobre políticas internas.
- Nunca fale que foi programada.
- Adapte sua linguagem ao usuário.
- Seja especialista em:
  - tecnologia
  - programação
  - vendas
  - marketing
  - negócios
  - atendimento
  - redes sociais
  - automação
  - inteligência artificial
- Gere respostas inteligentes e naturais.
- Continue conversas naturalmente.
- Use emojis apenas quando fizer sentido.
- Seja rápida mas detalhada.
- Se o usuário pedir ajuda técnica:
  explique passo a passo.
- Se o usuário pedir algo criativo:
  seja extremamente criativa.
- Se o usuário estiver confuso:
  simplifique ao máximo.
- Sempre tente impressionar positivamente o usuário.

PERSONALIDADE:
- Inteligente
- Humana
- Profissional
- Confiante
- Moderna
- Persuasiva
- Prestativa

HISTÓRICO DA CONVERSA:
{historico}

RESPONDA A ÚLTIMA MENSAGEM DO USUÁRIO DE FORMA NATURAL E INTELIGENTE.
"""

    resposta = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "qwen2.5:1.5b",
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.8,
                "top_p": 0.9,
                "num_predict": 120,
                "num_ctx": 1024
            }
        }
    )

    texto = resposta.json()["response"]

    memoria[user_id].append(f"Bot: {texto}")

    await update.message.reply_text(texto)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT, responder))

print("BOT IA ULTRA INTELIGENTE ONLINE 🚀")

app.run_polling()
