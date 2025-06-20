from django.db import models

from base.models import University, User


# Models for the chat app
class Ditch(models.Model):
    id = models.AutoField(primary_key=True)
    blocker = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocker')
    blocked = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blocked')
    ditched = models.BooleanField()


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipient')
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_messages'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
        ordering = ('-date',)

    # function gets all messages between 'the' two users (requires your pk and the other user pk)
    def get_all_messages(id_1, id_2):
        messages = []
        # get messages between the two users, sort them by date(reverse) and add them to the list
        message1 = Message.objects.filter(sender_id=id_1, recipient_id=id_2).order_by(
            '-date')  # get messages from sender to recipient
        for x in range(len(message1)):
            messages.append(message1[x])
        message2 = Message.objects.filter(sender_id=id_2, recipient_id=id_1).order_by(
            '-date')  # get messages from recipient to sender
        for x in range(len(message2)):
            messages.append(message2[x])

        # because the function is called when viewing the chat, we'll return all messages as read
        for x in range(len(messages)):
            messages[x].is_read = True
        # sort the messages by date
        messages.sort(key=lambda x: x.date, reverse=True)
        return messages

    # function gets all messages between 'any' two users (requires your pk)
    def get_message_list(u):
        # get all the messages
        m = []  # stores all messages sorted by latest first
        j = []  # stores all usernames from the messages above after removing duplicates
        k = []  # stores the latest message from the sorted usernames above
        for message in Message.objects.all():
            for_you = message.recipient == u  # messages received by the user
            from_you = message.sender == u  # messages sent by the user
            if for_you or from_you:
                m.append(message)
                m.sort(key=lambda x: x.sender.username)  # sort the messages by senders
                m.sort(key=lambda x: x.date, reverse=True)  # sort the messages by date

        # remove duplicates usernames and get single message(latest message) per username(other user) (between you and other user)
        for i in m:
            if i.sender.username not in j or i.recipient.username not in j:
                j.append(i.sender.username)
                j.append(i.recipient.username)
                k.append(i)

        return k

    # u == user_pk
    @staticmethod
    def get_connected_users(u):
        users = Message.objects.filter(sender=u)
        users2 = Message.objects.filter(recipient=u)
        l = set()
        for u in users:
            l.add(u.recipient)
        for u in users2:
            l.add(u.sender)
        #  convert set to list
        return list(l)

    # u == other user pk
    @staticmethod
    def get_last_message(current_user, u):
        messages = Message.objects.filter(sender=current_user).filter(recipient=u) | Message.objects.filter(
            sender=u).filter(recipient=current_user)
        messages = messages.order_by('-date')
        return messages[0]


class Study_Group(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    course_code = models.CharField(max_length=50)
    section = models.CharField(max_length=50)
    university = models.ForeignKey(University, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chat_study_groups'
        verbose_name = 'Study Group'
        verbose_name_plural = 'Study Groups'
        ordering = ('-date_created',)

    # function gets all participants in a Study_Group (requires Study_Group pk)
    @staticmethod
    def get_participants(id):
        return Participant.objects.filter(study_group=id)

    # function gets all chats a user is in (requires user pk)
    @staticmethod
    def get_chats(id):
        p = Participant.objects.filter(user=id)
        chats = []
        for i in p:
            chats.append(Study_Group.objects.get(id=i.study_group.id))
        return chats

    # function gets all messages in a Study_Group (requires Study_Group pk)
    @staticmethod
    def get_all_messages(id, current_user):
        # get messages in the chat, sort them by date(reverse) and add them to the list
        messages = Group_Message.objects.filter(study_group=id).order_by('-date')

        # because the function is called when viewing the chat, we'll return all messages as read
        for m in messages:
            rr = Read_Report.objects.create(user=current_user, message=m)
            rr.save()

        return messages

    # return study group if exist from course object
    def get_study_group(course):
        return Study_Group.objects.filter(course_code=course.course_code, section=course.section)[0]

    @staticmethod
    def get_unread_count(g_id, current_user):
        messages = Group_Message.objects.filter(study_group=g_id).order_by('-date')
        count = 0
        for m in messages:
            # it's not possible to have a message without a read report after the first seen message
            if not Read_Report.objects.filter(user=current_user, message=m).exists():
                count += 1
            else:
                break
        return count

    # function gets last messages in a Study_Group (requires Study_Group pk)
    @staticmethod
    def get_last_message(id):
        # get messages in the chat, sort them by date(reverse) and add them to the list
        messages = Group_Message.objects.filter(study_group=id).order_by('-date')
        if len(messages) > 0:
            return messages[0]
        else:
            return None


class Participant(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    study_group = models.ForeignKey('Study_Group', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username

    class Meta:
        db_table = 'chat_participants'
        verbose_name = 'Participant'
        verbose_name_plural = 'Participants'
        ordering = ('-date_joined',)


class Group_Message(models.Model):
    id = models.AutoField(primary_key=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    study_group = models.ForeignKey(Study_Group, on_delete=models.CASCADE)
    message = models.TextField(null=True, blank=True)
    attachment = models.FileField(upload_to='chat_attachments/', null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message

    class Meta:
        db_table = 'chat_group_messages'
        verbose_name = 'Group Message'
        verbose_name_plural = 'Group Messages'
        ordering = ('-date',)


class Read_Report(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.ForeignKey(Group_Message, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return ' seen on ' + str(self.date)

    class Meta:
        db_table = 'chat_read_reports'
        verbose_name = 'Read Report'
        verbose_name_plural = 'Read Reports'
        ordering = ('-date',)
