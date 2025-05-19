from django.db import models
from a_userauthapp.models import Voter_User

import hashlib
import json
import time

class Election(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='VoteChain-electionimage/', null=True)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Voter(models.Model):
    user = models.OneToOneField(Voter_User, on_delete=models.CASCADE)
    voter_id = models.CharField(max_length=100, unique=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


class Candidate(models.Model):
    POSITION = (
        ('President', 'President'),
        ('Vice President', 'Vice President'),
        ('Secretary', 'Secretary'),
        ('Treasurer', 'Treasurer'),
        ('Sport Director', 'Sport Director'),
    )

    election = models.ForeignKey(Election, on_delete=models.CASCADE, null=True)
    image = models.ImageField(upload_to='VoteChain-candidateimage/', null=True)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100, choices=POSITION, null=True)
    party = models.CharField(max_length=100)
    description = models.TextField(null=True)


class Vote(models.Model):
    voter = models.OneToOneField(Voter, on_delete=models.CASCADE)  # One vote per voter
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_hash = models.CharField(max_length=64, blank=True)  # Hash of blockchain transaction


class Block(models.Model):
    index = models.IntegerField()
    timestamp = models.FloatField()
    votes = models.TextField()  # JSON string of votes in the block
    previous_hash = models.CharField(max_length=64)
    hash = models.CharField(max_length=64)
    nonce = models.IntegerField(default=0)

    def compute_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "votes": self.votes,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

