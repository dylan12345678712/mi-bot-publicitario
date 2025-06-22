from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# Configuración
ADMIN_ID = 6115976248
TOKEN = "8050842324:AAEbFqDRr1-uTpQXMQ0x1oGVyjuALcABA1g"
GRUPO_COMPROBANTES = -1002829620923

# Canales disponibles
canales = [
    {
        "nombre": "🔹 DYLAN_1M 🎬🍿",
        "id": -1001945286271,
        "seguidores": "+150K",
        "descripcion": "🔥 Viral, masivo y de alto impacto",
        "enlace": "https://t.me/+C8xLlSwkqSc3ZGU5",
        "precios": {"12h": 20, "3d": 30, "7d": 50}
    },
    {
        "nombre": "🔹 Pelis & Series Gratis 🎞️",
        "id": -1002231546870,
        "seguidores": "+160K",
        "descripcion": "🎬 Público activo",
        "enlace": "https://t.me/+dpOprbZD6fFjMjhh",
        "precios": {"12h": 25, "3d": 60, "7d": 90}
    },
    {
        "nombre": "🔹 PELÍCULAS TIK TOK 🎬",
        "id": -1001632439981,
        "seguidores": "+90K",
        "descripcion": "📲 Contenido corto y viral",
        "enlace": "https://t.me/+V_dSWxm2rtdhNDNh",
        "precios": {"12h": 17, "3d": 25, "7d": 40}
    },
    {
        "nombre": "🔹 FILMS VISIONARIO 🍿",
        "id": -1002164527984,
        "seguidores": "+40K",
        "descripcion": "🎯 Audiencia 80% activa",
        "enlace": "https://t.me/+L4PH6Uxpa0E4ZGFh",
        "precios": {"12h": 18, "3d": 30, "7d": 50}
    },
    {
        "nombre": "🔹 Canal Económico 💰",
        "id": -1002253473475,
        "seguidores": "+20K",
        "descripcion": "⚡️ Barato, activo y efectivo",
        "enlace": "https://t.me/+-JPxhrGQxOgyNzUx",
        "precios": {"12h": 5, "3d": 15, "7d": 21}
    },
]

usuarios_pago_aprobado = {}
contador_pagos = {}

# /start con imagen y mensaje llamativo
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    keyboard = [["📢 Hacer Publicidad", "📬 Soporte"]]
    markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    texto = (
        "🎯 *¡Bienvenido a tu Bot Publicitario Premium!*\n\n"
        "🚀 Publica en nuestros canales con miles de seguidores activos.\n"
        "🎁 ¡Promoción 3x1! Por cada 3 pagos obtienes 1 publicación GRATIS.\n\n"
        "👇 Usa los botones para comenzar:"
    )

    with open("publicidad_banner.jpg", "rb") as img:
        await update.message.reply_photo(photo=img, caption=texto, parse_mode=ParseMode.MARKDOWN, reply_markup=markup)
# Mostrar canales
async def manejar_mensaje(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Texto junto a la imagen
    texto_canal = "📋 *Elige el canal donde publicarás tu anuncio:*\n\n"
    for canal in canales:
        texto_canal += (
            f"🔹🔹 *{canal['nombre']}*\n"
            f"++{canal['seguidores']} seguidores\n"
            f"[Ver canal]({canal['enlace']})\n\n"
        )

    # Enviar imagen con caption
    with open("canales_banner.jpg", "rb") as img:
        await ctx.bot.send_photo(
            chat_id=chat_id,
            photo=img,
            caption=texto_canal,
            parse_mode='Markdown'
        )

    # Botones para elegir canal
    botones = [
        [InlineKeyboardButton(canal["nombre"], callback_data=str(i))]
        for i, canal in enumerate(canales)
    ]

    await ctx.bot.send_message(
        chat_id=chat_id,
        text="Selecciona un canal de los botones de abajo 👇",
        reply_markup=InlineKeyboardMarkup(botones)
    )

# Selección de canal
async def canal_seleccionado(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    idx = int(update.callback_query.data)
    canal = canales[idx]
    ctx.user_data["canal_idx"] = idx

    precios = canal["precios"]
    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton(f"🕒 12 h — ${precios['12h']}", callback_data="duracion_12h")],
        [InlineKeyboardButton(f"📆 3 días — ${precios['3d']}", callback_data="duracion_3d")],
        [InlineKeyboardButton(f"🗓️ 7 días — ${precios['7d']}", callback_data="duracion_7d")]
    ])
    await update.callback_query.message.reply_text(
        f"⏰ Elige la duración para publicar en *{canal['nombre']}*:",
        parse_mode=ParseMode.MARKDOWN,
        reply_markup=botones
    )

# Elegir duración
async def elegir_duracion(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    duracion_key = query.data.split("_")[1]
    canal = canales[ctx.user_data["canal_idx"]]
    precios = canal["precios"]

    duracion_map = {"12h": "12 horas", "3d": "3 días", "7d": "7 días"}
    precio = precios[duracion_key]
    ctx.user_data["duracion"] = duracion_key
    ctx.user_data["precio"] = precio

    texto = (
        f"🧾 Canal seleccionado: *{canal['nombre']}*\n"
        f"⏳ Duración: {duracion_map[duracion_key]}\n"
        f"💰 Precio: ${precio}\n\n"
        "💡 Realiza el pago y luego pulsa *Ya pagué* para subir tu comprobante."
    )
    botones = InlineKeyboardMarkup([
        [InlineKeyboardButton("💸 Pagar (Binance)", switch_inline_query_current_chat="TPBbBjmtedKKst42MZCGbqNx4BhpuHDTHb")],
        [InlineKeyboardButton("💳 Pagar con PayPal", url="https://paypal.me/wilmerLenin?country.x=EC&locale.x=es_XC")],
        [InlineKeyboardButton("✅ Ya pagué", callback_data="pago_hecho")]
    ])
    await query.message.reply_text(texto, parse_mode=ParseMode.MARKDOWN, reply_markup=botones)

# Usuario marcó que pagó
async def marcar_pago(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["esperando_comprobante"] = True
    await update.callback_query.message.reply_text("📤 Envíame ahora tu comprobante de pago (imagen o captura).")

# Recibir comprobante
async def recibir_comprobante(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if ctx.user_data.get("esperando_comprobante") != True:
        return

    user_id = update.effective_user.id
    usuario = update.message.from_user
    canal_idx = ctx.user_data.get("canal_idx")
    duracion_key = ctx.user_data.get("duracion", "12h")

    if canal_idx is None:
        await update.message.reply_text("❌ Primero elige un canal.")
        return

    canal = canales[canal_idx]
    usuarios_pago_aprobado[user_id] = {
        "usado": False,
        "puede_publicar": True,
        "canal_id": canal["id"],
        "duracion": duracion_key
    }
    ctx.user_data["esperando_comprobante"] = False

    await ctx.bot.send_photo(
        chat_id=GRUPO_COMPROBANTES,
        photo=update.message.photo[-1].file_id,
        caption=(
            f"<b>📤 Nuevo comprobante de pago</b>\n"
            f"🧑 Usuario: @{usuario.username or usuario.first_name} (ID: <code>{user_id}</code>)\n"
            f"📢 Canal: {canal['nombre']}\n"
            f"⏱️ Duración: {duracion_key} — ${canal['precios'][duracion_key]}"
        ),
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Aprobar", callback_data=f"aprobar_{user_id}"),
            InlineKeyboardButton("❌ Rechazar", callback_data=f"rechazar_{user_id}")
        ]])
    )

    await update.message.reply_text("📩 Tu comprobante fue enviado para revisión.")

# Aprobar / Rechazar desde botón
async def manejar_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data

    if data.startswith("aprobar_"):
        user_id = int(data.split("_")[1])
        if user_id in usuarios_pago_aprobado:
            usuarios_pago_aprobado[user_id]["usado"] = False
            usuarios_pago_aprobado[user_id]["puede_publicar"] = True
            await ctx.bot.send_message(
                chat_id=user_id,
                text="✅ <b>Pago aprobado</b>\n\nYa puedes enviar <b>una sola publicación</b> para este canal.",
                parse_mode=ParseMode.HTML
            )
        await query.answer("Pago aprobado")

    elif data.startswith("rechazar_"):
        user_id = int(data.split("_")[1])
        usuarios_pago_aprobado.pop(user_id, None)
        await ctx.bot.send_message(
            chat_id=user_id,
            text="❌ <b>Pago rechazado</b>\n\nTu comprobante no fue aprobado. Contacta a @Dylan_1m_oficial para más información.",
            parse_mode=ParseMode.HTML
        )
        await query.answer("Pago rechazado")

    elif data == "reiniciar":
        await manejar_mensaje(update, ctx)

# Recibir anuncio
async def recibir_anuncio(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = usuarios_pago_aprobado.get(user_id)

    if not data or data["usado"]:
        await update.message.reply_text("❌ No puedes publicar. Compra o espera aprobación.")
        return

    canal_id = data["canal_id"]
    try:
        mensaje = await ctx.bot.copy_message(
            chat_id=canal_id,
            from_chat_id=update.message.chat_id,
            message_id=update.message.message_id
        )
        usuarios_pago_aprobado[user_id]["usado"] = True

        contador_pagos[user_id] = contador_pagos.get(user_id, 0) + 1
        restantes = max(0, 3 - (contador_pagos[user_id] % 3))

        texto = (
            "✅ <b>Anuncio publicado con éxito.</b>\n\n"
            "🎉 ¡Gracias por confiar en nuestro servicio!\n"
            f"🎁 Te faltan <b>{restantes}</b> compras para obtener una publicación GRATIS (promoción 3x1)."
        )
        botones = InlineKeyboardMarkup([[
            InlineKeyboardButton("🔍 Ver mi publicación", url=f"https://t.me/c/{str(canal_id)[4:]}/{mensaje.message_id}"),
            InlineKeyboardButton("➕ Comprar otra publicación", callback_data="reiniciar")
        ]])
        await update.message.reply_text(texto, parse_mode=ParseMode.HTML, reply_markup=botones)

    except:
        await update.message.reply_text("❌ Error al publicar. Contacta soporte.")

# Soporte
async def soporte(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📬 Soporte:\nHabla directamente con @Dylan_1m_oficial si necesitas ayuda o quieres asesoramiento personalizado.")

# MAIN
if __name__ == '__main__':
    import asyncio

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.Regex("(?i)publicidad"), manejar_mensaje))
    app.add_handler(MessageHandler(filters.Regex("(?i)soporte"), soporte))
    app.add_handler(CallbackQueryHandler(canal_seleccionado, pattern="^[0-9]+$"))
    app.add_handler(CallbackQueryHandler(elegir_duracion, pattern="^duracion_"))
    app.add_handler(CallbackQueryHandler(marcar_pago, pattern="^pago_hecho$"))
    app.add_handler(CallbackQueryHandler(manejar_callback, pattern="^(aprobar_|rechazar_|reiniciar).*"))
    app.add_handler(MessageHandler(filters.PHOTO & filters.CaptionRegex(".*"), recibir_anuncio))
    app.add_handler(MessageHandler(filters.PHOTO, recibir_comprobante))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, recibir_anuncio))

    print("✅ BOT INICIADO")
    app.run_polling()
