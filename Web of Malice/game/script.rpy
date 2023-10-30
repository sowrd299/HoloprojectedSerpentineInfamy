# The script of the game goes in this file.

# GRAPHICS UTILITY
init python:

    class LineDrawer(renpy.Displayable):

        def __init__(self, point1, point2, color):

            super().__init__()

            self.point1 = point1
            self.point2 = point2
            self.color = color

        def render(self, width, height, st, at):
            render = renpy.Render(width, height)
            canvas = render.canvas()
            canvas.line(self.color, tuple(self.point1), tuple(self.point2), 3)
            return render

    class Vec2():

        class VecIter():

            def __init__(self, vec):
                self.ind = 0
                self.vec = vec

            def __next__(self):
                if self.ind < 2:
                    r = (self.vec.x, self.vec.y)[self.ind]
                    self.ind += 1
                    return r
                else:
                    raise StopIteration

        def __init__(self,x,y):
            self.x = x
            self.y = y

        def __add__(self, other):
            other_vec = Vec2(*other)
            return Vec2(self.x + other_vec.x, self.y + other_vec.y)

        def __iter__(self):
            return self.VecIter(self)

# GAME LOGIC
init python:
    class HackTool():

        READ_TYPE = "Reader"
        WRITE_TYPE = "Scribe"
        TRAV_TYPE = "Traveler"

        def __init__(self, name, tool_type, breach, alert):
            self.name = name
            self.tool_type = tool_type
            self.breach = breach
            self.alert = alert

    class HackNode():

        def __init__(self, name, strength, start_alert, pos, description = ""):
            self.name = name
            self.pos = pos
            self.strength = strength
            self.alert = start_alert
            self.description = description

# GAME COMPONENTS
define cats_cradle_tool = HackTool("Cat's Craddle", HackTool.TRAV_TYPE, 40, 5)
define eye_tool = HackTool("Cat's Eye", HackTool.READ_TYPE, 30, 10)
define fountain_tool = HackTool("Black Fountain", HackTool.WRITE_TYPE, 20, 15)

define start_tools = [cats_cradle_tool, eye_tool, fountain_tool]

define ambriav_relay_node = HackNode("Ambriav Ninth Public Relay", 20, 30, Vec2(1100,1800), "One of the cheapest and most trafficked relays for data entering and leaving the planet Ambriav.")
define outer_relay_node = HackNode("Jupitav Outer Commerce Relay", 40, 35, Vec2(1500,1100), "One of the cheapest and most trafficked relays for data entering and leaving the planet Ambriav.")

define all_nodes = [ambriav_relay_node, outer_relay_node]
define all_node_links = [(ambriav_relay_node, outer_relay_node)]

# GAME UI
screen tool_button(tool):
    frame:
        has vbox
        
        textbutton tool.name
        text "[tool.tool_type]|[tool.breach]%|+[tool.alert]!"

screen node(node):
    frame xmaximum 400 xpos node.pos.x ypos node.pos.y:
        has vbox
        
        textbutton "[node.name] [[[node.strength]%|[node.alert]!]"
        text node.description


screen hack(start_node):

    $ current_node = start_node

    #text "[hack_name]" xalign 0.5
    side "c b" xalign 0.5:

        viewport draggable True child_size(3000,3000) xinitial start_node.pos.x yinitial start_node.pos.y:
            for node1, node2 in all_node_links:
                add LineDrawer(node1.pos + (200,100), node2.pos + (200,100), (20,40,160))
            for node in all_nodes:
                use node(node)

        grid len(start_tools) 1 xalign 0.5 yalign 1 spacing 8:
            for tool in start_tools:
                use tool_button(tool)

    textbutton "End Connection" action Return() xalign 0.9 yalign 0.1


# CHARACTERS
define petra = Character("Petra u·Fari")
define receptionist = Character("Receptionist")
define first_client = Character("Client")
define enri = Character("Enri d·Jul")
define tor = Character("Tor")


# THE SCRIPT
label start:

    # Show a background. This uses a placeholder by default, but you can
    # add a file (named either "bg room.png" or "bg room.jpg") to the
    # images directory to show it.

    scene bg space

    # These display lines of dialogue.

    receptionist """Hello, this is [receptionist] with Veritas Incorporated speaking, how may I help you? 
    Oh, mhm, I see. Are you sure? Alright. Let me see if she’s in. Ms. u·Fari, we’ve got a client on the line!"""
    receptionist """Says it’s a job but it involves a rather personal matter, won’t tell me what it is, wants to speak with you directly. 
    Shall I patch her through or are you “not here”?"""
    menu:
        "I’m in a good mood. Put her through!" :
            pass
    receptionist """Are you sure? 
    This “personal matter” wouldn’t be another angry woman who’s girlfriend you stole away during a night of drunken debauchery, would it?"""
    menu:
        "Oh c’mon, that only happened one time! How was I supposed to know that they were engaged? \
        Anyway I promise, I’ve been an angel recently. I want to hear more about this mysterious job.":
            pass
    receptionist """As you wish."""

label first_client:

    first_client "Are you Petra u Fari?"
    menu:
        "The one and only, my dear! Now, what can I do for you?":
            pass
    first_client """You see I had this boyfriend for a while, met him on DATING APP. 
    I thought I’d found true love. But it seems he was more interested in screwing the woman who insert way of knowing people here. """ 
    first_client """Tragic, really, so I couldn’t think of anything to do but the obvious."""
    menu: 
        "I’m hearing you loud and clear. I can transfer all his bank funds to the corrupt politician of your choice by the end of the evening, \
        leaving him penniless and with some uncomfortable questions about his political leaning. \
        Or I could always make sure the next shuttle he takes off world “gets lost” and finds itself trying to cross through the Haro blockade. \
        Ooooh or I could third thing.":
            pass
    first_client "What!? No no, I just want you to hack into his DATING APP profile."
    menu:
        "Oh… that’s it?":
            pass
    first_client "Well I’d want you to change his profile to say “I’m a filthy lying, cheating scumbag who can’t be trusted.”"
    menu:
        "Nothing else?":
            pass
    first_client "I suppose I’d appreciate it if you made it hard for him to change back."

    call screen hack(ambriav_relay_node)

label meet_houses:

    menu:
        "Anything interesting going on?":
            pass
    enri "Governor’s dead."
    menu:
        "Again? I said something interesting.":
            pass
    enri "Killed by an assassin?"
    menu:
        "Do you not understand the word interesting?":
            pass
    tor "It’s rumored that the assassin was from house Calitus."
    menu:
        "Okay now we’re talking. What did they do, sing him to death? Interpretive dance until he lost his will to live?":
            pass
    enri "Yeah you’d expect this from House Grim, House Blai, House Avond - regardless of the fact that the governor was a member -"
    menu:
        "House Malituse would make it look like you’d never even existed in the first place.":
            pass
    enri "But Calitus doesn’t usually get their hands this dirty. Must be important, whatever reason they have. Kind of the house you’d least expect."
    tor "I don’t know, It could have been House Rose."
    menu:
        "Boo that’s cheating, they’re not even a major house.":
            pass
    tor "No one ever said anything about major or minor houses! I’m just saying that you don’t tend to expect cunning assassinations from sex cults!"
    enri "Have you never heard of a honey pot? Anyway I would hardly call House Rose a cult. They keep things very proper and business-like."
    menu:
        "In fairness to them, theirs is the most legitimate “business” out of the houses I can think of. Hardly even illegal.":
            pass
    tor "What about Haro?"
    enri "What about them?"
    tor "Well, they’re the only major house we haven’t mentioned. What are their odds on assassination?"
    enri "Killing their opponents seems pretty much to be their MO."
    menu:
        "Yeah but sneaking around to do it isn’t. I don’t know if you can call it assassination when they just kill you to your face, no frills or tricks about it.":
            pass

    # This ends the game.

    return