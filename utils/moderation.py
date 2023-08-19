import discord


def get_modlog_kick_ban_msg(bot, user, moderator, reason, msg_type):
    """
    Creates discord.Embed message for mod-logs channels for ban events

    # Returns

    mod_log_ban_message {discord.Embed} : Embed message to be sent in the
                                           mod-logs channel
    """

    user_avatar = user.avatar

    mod_log_ban_message = discord.Embed(color=discord.Color.from_rgb(225, 198, 153))

    if msg_type == 1:
        mod_log_ban_message.set_author(
            name="Ha sido baneado " + str(user),
            icon_url=user_avatar
        )
    elif msg_type == 2:
        mod_log_ban_message.set_author(
            name="[Unbanned] " + str(user),
            icon_url=user_avatar
        )
    elif msg_type == 3:
        mod_log_ban_message.set_author(
            name="[Kicked] " + str(user),
            icon_url=user_avatar
        )

    mod_log_ban_message.add_field(
        name='Usuario',
        value=f'{user.mention}', inline=False)

    mod_log_ban_message.add_field(
        name='Responsable',
        value=f'{moderator.mention}', inline=False)

    mod_log_ban_message.add_field(
        name='Razón',
        value=reason, inline=False)

    return mod_log_ban_message
