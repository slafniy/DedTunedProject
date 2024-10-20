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


## Changelist
### Exhaustion - new mechanics (WIP)
A new mechanics which forces party to rest more often. 
  
In a combat characters will get Tiredness stacks, which on some point lead to various consequences:
- Level 1 (20+ stacks): slight fatigue. A penalty to attack rolls, saving throws, ability checks, skill checks and spell DC
- Level 2 (30+ stacks): Uncontrollable sleep. Every turn character must perform CON saving throw or will fall asleep for 2 turns
- Level 3 (50+ stacks): Death.

Long Rest (with supplies) removes all Tiredness stacks, Short Rest removes 20.

Note: Not a direct adaptation of dnd5e Exhaustion and I'm not going to do direct replica. 
TBH I invented it in my head first and found that dnd already has something like that second.

Note 2: I haven't tested this long term yet, so it could be not balanced, most probably too weak :)


### Experience reward
Required XP per level increased (around +27% total) because of two reasons:
- Do not let player to over-level enemies too much
- Bring more sense to XP rewards in Act III (in stock game player reaches level 12 at the beginning of Act III and progress stops)  

Expected levels:
 - 5 at the Act I before Rosymorn Monastery 
 - 6 at the end of Act I
 - 8 at the end of Act II 
 - 12 at the end of Act III


### Pickpocketing
- You cannot pickpocket Volo and Jergal anymore

Note: pickpocketing without any risk doesn't make sense.


### Honor mode boost
- HP boost increased from 30% to 160% (x2 HP from stock Honor)
- Honor attack roll bonus for almost all enemies increased from 2 to 3
- Zhalk now has 300hp (was 195)
- Raphael HP set to 1666

Note: HP boost should give a chance for enemies to use their abilities and not being slain on first turn. 
I'm tuning HP for some bosses, so not all of them will have +160% boost.  
Attack bonus should make enemies slightly more dangerous.


### Multiclassing
- Multiclassing is forbidden

Note: first, it's impossible to balance out Multiclassing with my experience, knowledge and tools. 
Second, I personally don't like it as a concept because it looks like abusing combination of too strong low-level features which are essential for pure class and could not be nerfed too much.
Proper multiclassing should include some lore limitations, karma mechanics of something else, which is not the case in BG3.


### Resting
- Long rest cost increased to 250
- You cannot use Partial Rest

Note: It is currently working by disabling "Long Rest" button if you have less than 250 supplies.
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

Also fixed vanilla "feature" that such buffs remains after re-spec on any person except caster itself - now re-spec removes them from everyone.


### Feats
Feats do not provide Ability increase bonus anymore. 
Instead, you have Ability +1 bonus every 3rd level.



#### Ability Improvement
Removed from the game.



#### Abnormal Obstinacy - NEW FEAT
The number you need to roll a Critical Hit reduces by 1 every time you hit the same target in 
melee. You should not use Two-Handed or  Versatile weapon holding it in two hands. The effect 
lasts until you roll Critical Hit or your turn ends. Stacks up to 5 times.

Note: This is an option for one-handed and dual builds to compete against GWM.


#### Tavern Brawler
- Does not add attack roll bonus  

Note: it`s pretty strong damage boost for one feat, an attack roll bonus makes it imbalanced.


#### Great Weapon Master
- Attack roll penalty reduced to -3 (was -5) for levels 4-7
- Damage bonus reduced to 6 (was 10) for levels 4-7

Note: this is both too strong damage bonus for low levels if you managed to overcome attack roll penalty and too weak if you don't.
This change slightly balances it.


#### War Caster 
- You also can pick INT, WIS or CHA +1 bonus  

Note: this is must have feat for any caster on low levels, but it's painful to pick this only for utility without any other bonus (no, reaction focus does not make it any better). 
Also, there are too few feats with stat bonus for casters comparing to non-casters.


#### Sharpshooter 
- Attack roll penalty reduced to -3 (was -5) for levels 4-7
- Damage bonus reduced to 6 (was 10) for levels 4-7

Note: same changes due to same reasons as for Great Weapon Master.


### Spells
- Branding Smite (both Paladin and Tiefling versions) does not consume Bonus Action and does not require concentration
- Searing Smite (both Paladin and Tiefling versions) does not consume Bonus Action and does not require concentration
- Thunderous Smite does not consume Bonus Action
- Wrathful Smite does not consume Bonus Action and does not require concentration
- Divine Favour does not require concentration but lasts 2 turns
- Flame Blade does not require concentration and lasts until Long Rest
- Shadow Blade (from item) does not require concentration
- Barkskin does not require concentration (but works only for party members)
- Heroism does not require concentration but lasts only 3 turns
- Phantasmal Force does not require concentration but lasts only 5 turns
- Flaming Sphere does not require concentration
- Web does not require concentration
- Sleep Maximum Total Target HP increased (x1.5) because enemies have more HP in mod
- Animate Dead - lasts only 10 turns
- Conjure Elemental - lasts only 10 turns
- Planar Ally - lasts only 10 turns


### Classes
#### Fighter Champion 
- Improved Critical passive gives -2 critical threshold instead of -1

Note: this subclass is too weak comparing to Battle Master, so I bring him this buff.



#### Barbarian
- Rage does not consume Bonus Action
- Enraged Throw now gives stack of Frenzied Strain as Frenzied Strike always does.

Note: throwing build for Berserker is insanely strong, this change alongside of Tavern Brawler nerf should calm down it a little.


#### Cleric War Domain 
- War Priest Action Points reset on Short Rest instead of Long Rest  
Note: additional attack as bonus action isn't THAT strong.


### Equipment
#### Arrow of Many Targets
- Renamed to Arrow of Ricochet
- Now only affects one additional target in 9 meters range

Note: it was insanely strong


#### Hat of Fire Acuity
Now stacks buff only up to 5 stacks (was 10)