import discord


def get_modlog_kick_ban_msg(bot, user, moderator, reason, msg_type):
    """
    Creates discord.Embed message for mod-logs channels for ban events

    # Returns

    mod_log_ban_message {discord.Embed} : Embed message to be sent in the
                                           mod-logs channel
    """

    user_avatar = user.avatar_url

    mod_log_ban_message = discord.Embed()

    if msg_type == 1:
        mod_log_ban_message.set_author(
            name="[Banned] " + str(user),
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
        name='User',
        value=f'{user.mention}', inline=True)

    mod_log_ban_message.add_field(
        name='Moderator',
        value=f'{moderator.mention}', inline=True)

    mod_log_ban_message.add_field(
        name='Reason',
        value=reason, inline=True)

    return mod_log_ban_message

async def user_ban(user: discord.abc.User, guild: discord.Guild):
    await guild.ban(user, "test", 3)
    print(user.global_name + " baneado!")