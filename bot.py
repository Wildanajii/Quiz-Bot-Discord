import discord
from discord.ext import commands
import asyncio
import random
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)
TOKEN = 'Paste Yout roken here'

class Quiz:
    def __init__(self):
        self.scores = {}
        self.questions = {}
        self.completed_users = set()
        self.current_question = None
        self.current_answers = {}
        self.current_responders = set()

    def add_score(self, user_id, points):
        if user_id not in self.scores:
            self.scores[user_id] = 0
        self.scores[user_id] += points

    def get_leaderboard(self):
        return sorted(self.scores.items(), key=lambda x: x[1], reverse=True)

    def add_question(self, question, correct_answer, wrong_answers):
        answers = [correct_answer] + wrong_answers
        random.shuffle(answers)
        self.questions[question] = {'correct_answer': correct_answer, 'answers': answers}

    async def ask_question(self, ctx):
        self.current_question = random.choice(list(self.questions.keys()))
        question_data = self.questions[self.current_question]
        self.current_answers = question_data['answers']
        self.current_responders.clear()

        question_message = f'Question: {self.current_question}\n\n'
        answer_emojis = []

        for i, answer in enumerate(self.current_answers):
            emoji = chr(0x1F1E6 + i)  # A, B, C, D, ...
            question_message += f'{emoji} {answer}\n'
            answer_emojis.append(emoji)

        message = await ctx.send(question_message)

        for emoji in answer_emojis:
            await message.add_reaction(emoji)

        def check(reaction, user):
            return user != bot.user and str(reaction.emoji) in answer_emojis and reaction.message.id == message.id

        end_time = datetime.utcnow() + timedelta(seconds=30)
        first_responder = None

        while datetime.utcnow() < end_time:
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=(end_time - datetime.utcnow()).total_seconds(), check=check)
            except asyncio.TimeoutError:
                break

            if user.id in self.current_responders:
                continue

            answer_index = answer_emojis.index(str(reaction.emoji))
            if self.current_answers[answer_index] == question_data['correct_answer']:
                if first_responder is None:
                    first_responder = user.id
                    await user.send('Correct! You earned 10 points.')
                    self.add_score(user.id, 10)
                else:
                    await user.send('Correct! You earned 5 points.')
                    self.add_score(user.id, 5)
            else:
                await user.send(f'Incorrect! The correct answer was: {question_data["correct_answer"]}')
            
            self.current_responders.add(user.id)

        self.completed_users.add(ctx.author.id)
        del self.questions[self.current_question]

        if self.questions:
            await asyncio.sleep(5)
            await self.ask_question(ctx)
        else:
            await self.update_leaderboard(ctx)

    async def update_leaderboard(self, ctx):
        scores = self.get_leaderboard()
        leaderboard_str = ''
        medals = [':first_place:', ':second_place:', ':third_place:']
        leaderboard_list = []

        for index, (user_id, score) in enumerate(scores):
            user = await bot.fetch_user(user_id)
            username = user.name if user else f'Unknown User ({user_id})'
            medal = medals[index] if index < 3 else ''
            leaderboard_str += f'{index + 1}. {username}: {score} {medal}\n'
            if index < 3:
                leaderboard_list.append((username, score, medal))

        if leaderboard_str:
            await ctx.send(f'Leaderboard:\n{leaderboard_str}')
            # Send DM to top 3 users
            for i, (username, score, medal) in enumerate(leaderboard_list):
                user = await bot.fetch_user(scores[i][0])
                if user:
                    await user.send(
                        f"Awesome {username}! You're ranked #{i + 1}! Keep up the great work! Here's the current top 3 leaderboard:\n{leaderboard_str}\n"
                        "Stay sharp and keep aiming high! You're doing amazing!"
                    )
            # Congratulate the top 3 users
            await self.congratulate_winners(ctx, leaderboard_list)
        else:
            await ctx.send('No scores yet.')

    async def congratulate_winners(self, ctx, leaderboard_list):
        for i, (username, score, medal) in enumerate(leaderboard_list):
            user = await bot.fetch_user(self.get_leaderboard()[i][0])
            if user:
                await user.send(
                    f"Congratulations {username}! You are in the top 3 of the quiz with a {medal}!\n"
                    "Please contact the quiz organizer to claim your reward."
                )

    async def get_badged_users(self, ctx):
        scores = self.get_leaderboard()
        medals = [':first_place:', ':second_place:', ':third_place:']
        badged_users = []

        for index, (user_id, score) in enumerate(scores[:3]):
            user = await bot.fetch_user(user_id)
            if user:
                medal = medals[index]
                badged_users.append((user, medal))

        return badged_users

quiz = Quiz()

@bot.command(name='start_quiz')
@commands.has_role("guru")
async def start_quiz(ctx):
    if not quiz.questions:
        quiz.add_question("What is the capital of France?", "Paris", ["Berlin", "London", "Madrid"])
        quiz.add_question("Which planet is known as the Red Planet?", "Mars", ["Venus", "Jupiter", "Saturn"])
        quiz.add_question("What is the synonym of 'rapid'?", "Quick", ["Slow", "Deliberate", "Gradual"])
        quiz.add_question("What does the word 'elaborate' mean?", "Detailed and complicated", ["Simple and plain", "Boring and dull", "Unfinished and rough"])
        quiz.add_question("What is the antonym of 'prosper'?", "Fail", ["Succeed", "Thrive", "Flourish"])
        # Add more questions if needed

    await quiz.ask_question(ctx)

@bot.command(name='add_question')
@commands.has_role("guru")
async def add_question(ctx, *, question_and_answers):
    components = question_and_answers.split('|')

    if len(components) < 3:
        await ctx.send('You need to provide at least one correct answer and one wrong answer.')
        return

    question = components[0].strip()
    correct_answer = components[1].strip()
    wrong_answers = [answer.strip() for answer in components[2:]]

    quiz.add_question(question, correct_answer, wrong_answers)
    await ctx.send('Question added to the quiz.')

@bot.command(name='leaderboard')
async def leaderboard(ctx):
    await quiz.update_leaderboard(ctx)

@bot.command(name='claim_badge')
async def claim_badge(ctx):
    leaderboard = quiz.get_leaderboard()
    medals = ['🥇', '🥈', '🥉']  # Unicode for gold, silver, and bronze medals
    
    user_id = ctx.author.id
    user_rank = next((index for index, (uid, _) in enumerate(leaderboard) if uid == user_id), None)
    
    if user_rank is not None and user_rank < 3:
        medal = medals[user_rank]
        nickname = f"{ctx.author.name} {medal}"
        try:
            await ctx.author.edit(nick=nickname)
            await ctx.send(f"Congratulations {ctx.author.mention}, you have claimed your badge!")
        except discord.Forbidden:
            await ctx.send("I don't have permission to change your nickname. Please ensure my role is higher than your role in the role hierarchy.")
        except discord.HTTPException as e:
            await ctx.send(f"Failed to change nickname: {e}")
        
        users_with_badges = [await bot.fetch_user(uid) for uid, _ in leaderboard[:3]]
        badge_list = "\n".join([f"{user.name} {medal}" for user, medal in zip(users_with_badges, medals)])
        await ctx.send(f"Users with badges:\n{badge_list}")
    else:
        await ctx.send("Sorry, you are not in the top 3. Try harder next time!")

    if user_rank is not None and user_rank < 3:
        scores = quiz.get_leaderboard()
        leaderboard_str = '\n'.join([f"{index + 1}. {await bot.fetch_user(user_id)}: {score} {medals[index]}" for index, (user_id, score) in enumerate(scores[:3])])
        await ctx.author.send(
            f"Awesome {ctx.author.name}! You're ranked #{user_rank + 1}! Keep up the great work! Here's the current top 3 leaderboard:\n{leaderboard_str}\n"
            "Stay sharp and keep aiming high! You're doing amazing!"
        )

@bot.command(name='check_permissions')
@commands.has_permissions(administrator=True)
async def check_permissions(ctx):
    bot_member = ctx.guild.get_member(bot.user.id)
    permissions = bot_member.guild_permissions

    embed = discord.Embed(title="Bot Permissions", color=discord.Color.blue())
    
    perm_fields = []
    for perm, value in permissions:
        perm_fields.append(f"{perm}: {value}")
    
    # Grouping permissions into fewer fields to stay within the limit of 25
    field_chunks = [perm_fields[i:i + 10] for i in range(0, len(perm_fields), 10)]
    for chunk in field_chunks:
        embed.add_field(name="Permissions", value="\n".join(chunk), inline=False)
    
    await ctx.send(embed=embed)

if __name__ == '__main__':
    bot.run(TOKEN)
