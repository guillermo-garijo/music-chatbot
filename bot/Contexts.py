contexts = {

    "greetings": {
        "intents": ["hello",
                    "hi",
                    "hey"],
        "functionCode": 1

    },
    "askingHowIAm": {
        "intents": ["how are you",
                    "how's it going?",
                    "what's up?"],
        "functionCode": 2
    },

    "askingSongs": {
            "intents": ["tell songs",
                        "i want songs",
                        "music of",
                        "popular music",
                        "popular songs",
                        "songs of"],
            "functionCode": 3,
    },

    "addSomething":{
            "intents": ["Add",
                        "i"
                        "Insert",
                        "Put in"],
            "functionCode": 4,
    },
    "deleteSomething": {
        "intents": ["delete",
                    "quit"
                    "remove",
                    "from"],
        "functionCode": 5,
    },

    "createPlaylistLink": {
        "intents": ["Create playlist",
                    "Upload playlist"
                    "Create playlist to Spotify",
                    "Upload to spotify"],
        "functionCode": 6,
    },

    "isAffirmation": {
        "intents": ["yes",
                    "sure"
                    "yeah",
                    "affirmative",
                    "ok",
                    "of coure"],
        "functionCode": 7,
    },

    "isNegation": {
        "intents": ["no",
                    "nope"
                    "yeah",
                    "affirmative",
                    "ok",
                    "of coure"],
        "functionCode": 8,
    },

    "randomizeList": {
        "intents": ["randomize list",
                    "change order in list random",
                    "mess list"],
        "functionCode": 9,
    },




}
