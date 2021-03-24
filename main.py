from Vk_bot import bot
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.utils import get_random_id
import vk_api
import config
print('started')
vk_session = vk_api.VkApi(token=config.VK_TOKEN)
longpoll = VkBotLongPoll(vk_session, '173391069')
lsvk = vk_session.get_api()
for event in longpoll.listen():
	if event.type == VkBotEventType.MESSAGE_NEW:
		
		print('New message:' + str(event.obj.text))
		print(f'For me by: {event.obj.from_id}')
		vkbot = bot(event.obj.from_id)
		text = event.obj.text
		try:
			lsvk.messages.send(
					user_id = event.obj.from_id,
					message = vkbot.new_message(text),
					random_id = get_random_id(),
					peer_id = event.obj.peer_id,
					keyboard =  vkbot.keyboard(event.obj.from_id)
					)
		except:
			print('ERROR')

			
		print('text:' + event.obj.text)

