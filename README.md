# DedTuned balance mod for Larian's Baldur's Gate 3 (WIP)
The final goals of this mod:
- Make Honor mode slightly harder
- Eliminate as many abuses as possible (WIP)
- Make too weak abilities stronger (WIP)
- Make too strong abilities weaker (WIP)
- Balance out need of resting for different classes (WIP)

This mod is a result of my 1200+ hours in BG3, big part of which was played with friends in my party.

Vanilla Honor is too simple IMO (I got Honor achievement with first try, 
knowing almost nothing about DnD), and also I'm a little bit annoyed that some of my buddies overuse 
every cheesy mechanics they found and I have to wait when they use EVERY buff from camp :)

So this is an attempt to make the game ideal for me. I have no goal to do it for vast audience,
if it's even possible, but I would appreciate if you guys try it and share your opinion in comments.

Mod page: https://mod.io/g/baldursgate3/m/dedtuned

## Changelist
### Exhaustion - new mechanics (WIP)
A new mechanics which forces party to rest more often. 
  
In a combat characters will get Tiredness stacks, which on some point lead to various consequences:
- Level 1 (15+ stacks): slight fatigue. A penalty to attack rolls, saving throws, ability checks, skill checks and spell DC
- Level 2 (25+ stacks): Uncontrollable sleep. Every turn character must perform CON saving throw or will fall asleep for 2 turns
- Level 3 (40+ stacks): Death.

Long Rest (with supplies) removes all Tiredness stacks, Short Rest removes 10.

Note: Not a direct adaptation of dnd5e Exhaustion and I'm not going to do direct replica. 
TBH I invented it in my head first and found that dnd already has something like that second.


### Experience reward
Required XP per level increased. Motivation:
- Do not let player to over-level enemies too much
- Bring more sense to XP rewards in Act III (in stock game player reaches level 12 at the beginning of Act III and progress stops)  

Expected levels:
 - 5 at the Act I before Rosymorn Monastery 
 - 6 at the end of Act I
 - 8 at the end of Act II 
 - 12 at the end of Act III


### Respec
- Respec cost is 1000 gold
- Every origin character has one-time free respec button

Note: I made this mainly to avoid exploiting of (almost free) resource regeneration after respec.


### Pickpocketing
- You cannot pickpocket Volo and Jergal anymore
- You cannot endlessly pickpocket one person, you will get a Sleight of Hand debuff (resets on Long Rest)

Vanilla pickpocketing is too easy, and to pickpocket a camp members is nonsense.


### Honor mode boost
- HP boost increased from +30% to range +100-200% (more for high level creatures)
- Honor attack roll bonus for high level enemies increased from 2 to 3
- HP for some bosses is increased manually

HP boost should give a chance for enemies to use their abilities and not being slain on first turn.


### Multiclassing
- Multiclassing is forbidden

First, it's impossible to balance out Multiclassing with my experience, knowledge and tools. 
Second, I personally don't like it as a concept because it looks like an abusing combination of too strong low-level features which are essential for pure class and could not be nerfed too much.
Proper multiclassing should include some lore limitations, karma mechanics of something else, which is not the case in BG3.


### Resting
- Long rest cost increased to 250
- You cannot use Partial Rest

Known issue: It is currently working by disabling "Long Rest" button if you have less than 250 supplies.
"Partial Rest" button is removed, you just cannot rest if you do not choose enough supplies, so be careful and 
don't destroy them if you already triggered end of the day :)


### Buffs from camp 
Most common until-long-rest buffs now works only if Caster and Target are in one party. Buff disappears if caster and target aren't the same person and aren't in party. Affected buffs:
- Bardic Inspiration (all versions)
- Longstrider
- Warding Bond (known issue: buff remains active on caster but paired person correctly loses it)
- Mage Armor
- Darkvision
- Freedom of Movement
- Aid
- Heroes Feast (Thoroughly Stuffed)
- Protection From Poison
- Barkskin

Also fixed vanilla "feature" that such buffs remains after re-spec on any person except caster itself - now re-spec removes them from everyone.


### Feats
Feats do not provide Ability increase bonus anymore. 
Instead, you have Ability +1 on level 7 and +2 on level 11.

I added new and changed some old feats to make different weapon build viable. 
Duals and single-handed weapon builds are stronger than in vanilla.



#### Ability Improvement
Removed from the game.


#### Abnormal Obstinacy - NEW FEAT
The number you need to roll a Critical Hit reduces by 1 every time you hit the same target in 
melee. You should not use Two-Handed or  Versatile weapon holding it in two hands. The effect 
lasts until you roll Critical Hit or your turn ends. Stacks up to 5 times.

Note: This is an option for one-handed and dual builds to compete against GWM.


#### Ambidextrous - NEW FEAT
Once per turn after making an offhand melee attack can make an additional one for free.

Note: this is a decent buff for Dual builds.


#### Duelist Mage - NEW FEAT
You can cast a cantrip (except Eldritch Blast) as a bonus action after making a melee attack 
with weapon you are proficient with. Your left hand should be free.

Note: this is a boost for Arcane Trickster, Warlock and anyone else who has a cantrip and use single-handed weapon without a shield.


#### Tavern Brawler
- Does not add attack roll bonus  

Note: it`s pretty strong damage boost for one feat, an attack roll bonus makes it imbalanced.


#### Great Weapon Master
- Attack roll penalty reduced to -3
- Damage bonus reduced to 6
- You can use additional attack only once per combat

Note: it is still strong damage boost, but not imbalanced.


#### Sharpshooter 
- Attack roll penalty removed
- Works only for weapon in main hand
- Damage bonus is your DEX modifier
- Costs 4m of Movement for every shot

Note: now it's not a copy-paste of GWM, and cannot be abused with one-handed crossbows.


##### Durable
- Protects from critical hits

Note: critical hit mechanics forces you to use anti-crit equipment, but it is limited. 
This feat is an option for those who wants to have extra protection and don't want to use anti-crit equipment.



### Spells
- **Smite spells**: do not require concentration, can be upcasted and deal more damage (except Divine)
- **Divine Favour**: does not require concentration
- **Flame Blade**: does not require concentration and lasts until Long Rest
- **Shadow Blade (from item)**: does not require concentration
- **Barkskin**: does not require concentration (but works only for party members)
- **Heroism**: does not require concentration but lasts only 3 turns
- **Phantasmal Force**: does not require concentration but lasts only 5 turns
- **Flaming Sphere**: does not require concentration
- **Web**: does not require concentration
- **Sleep, Color Spray, Power Word Kill**: maximum total target HP increased (x1.5) (because enemies have more HP)
- **Animate Dead**: lasts only 10 turns
- **Conjure Elemental**: lasts only 10 turns
- **Planar Ally**: lasts only 10 turns
- **Longstrider**: now an AOE spell
- **Protection From Energy**: does not require concentration
- **Grant Flight**: does not require concentration
- **Fog Cloud**: does not require concentration, lasts 3 turns
- **Faerie Fire**: does not require concentration, lasts 3 turns
- **Darkness**: does not require concentration, lasts 5 turns, upcast increases area
- **Dancing Lights**: does not require concentration
- **Blur**: does not require concentration, lasts 2 turns, upcast increases duration by 1 turn
- **Ray Of Enfeeblement**: does not require concentration, lasts 5 turns, deals initial 2d8 necrotic damage, upcast increases damage by 1d8
- **Stoneskin**: does not require concentration, lasts 10 turns
- **Bestow Curse**: does not require concentration
- **Protection From Evil And Good**: no concentration, lasts 10 turns, applies in AOE
- **Bless**: no concentration, lasts 3 turns
- **Bane**: no concentration, lasts 3 turns
- **Beacon Of Hope**: no concentration, upcast increases area
- **Resistance**: no concentration, lasts 3 turns


### Classes
#### Fighter Champion 
- Improved Critical passive gives -2 critical threshold instead of -1

Note: this subclass is too weak comparing to Battle Master, so I bring him this buff.


#### Barbarian
- Rage and End Rage does not consume Bonus Action
- Enraged Throw now gives stack of Frenzied Strain as Frenzied Strike always does.

Note: throwing build for Berserker was insanely strong, this change alongside of Tavern Brawler nerf should calm down it a little.


#### Cleric War Domain 
- War Priest Action Points reset on Short Rest instead of Long Rest  
Note: additional attack as bonus action isn't THAT strong.


### Equipment
#### Potions
- Elixir of Hill Giant Strength now gives +2 STR up to 22
- Elixir of Cloud Giant Strength now gives +6 STR up to 26
- All healing potions take an Action for use and could not be thrown to an ally,
but you can use it on ally in melee range


#### Arrow of Many Targets
- Renamed to Arrow of Ricochet
- Now only affects one additional target in 9 meters range

Note: it was insanely strong.


#### Hat of Fire Acuity
Now stacks buff only up to 5 stacks (was 10)


#### Enraging Heart Garb
Now works :)
