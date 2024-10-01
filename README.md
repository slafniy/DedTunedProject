# DedTuned balance mod for Larian's Baldur's Gate 3 (WIP)
The final goals of this mod:
- Make Honor mode slightly harder
- Eliminate as many abuses as possible (WIP)
- Make too weak abilities stronger (WIP)
- Make too strong abilities weaker (WIP)
- Balance out need of resting for different classes (WIP)

## Changelist
### Experience reward
Required XP per level increased (around +27% total) because of two reasons:
- Do not let player to over-level enemies too much
- Bring more sense to XP rewards in Act III (in stock game player reaches level 12 at the beginning of Act III and progress stops)  

Expected levels:
 - 5 at the Act I before Rosymorn Monastery 
 - 6 at the end of Act I
 - 8 at the end of Act II 
 - 12 at the end of Act III

### Feats
#### Tavern Brawler (verified)
- Does not add attack roll bonus  

Note: it`s pretty strong damage boost for one feat, an attack roll bonus makes it imbalanced.

#### Great Weapon Master (verified)
- Attack roll penalty reduced to -3 (was -5) for levels 4-7
- Damage bonus reduced to 6 (was 10) for levels 4-7

Note: this is both too strong damage bonus for low levels if you managed to overcome attack roll penalty and too weak if you don't.
This change slightly balances it.

#### War Caster (verified)
- You also can pick INT, WIS or CHA +1 bonus  

Note: this is must have feat for any caster on low levels, but it's painful to pick this only for utility without any other bonus (no, reaction focus does not make it any better). 
Also, there are too few feats with stat bonus for casters comparing to non-casters.

#### Sharpshooter (verified)
- Attack roll penalty reduced to -3 (was -5) for levels 4-7
- Damage bonus reduced to 6 (was 10) for levels 4-7

Note: same changes due to same reasons as for Great Weapon Master.

### Classes
#### Fighter Champion (verified)
- Improved Critical passive gives -2 critical threshold instead of -1

Note: this subclass is too weak comparing to Battle Master, so I bring him this buff.

#### Barbarian Berserker (verified)
- Enraged Throw now gives stack of Frenzied Strain as Frenzied Strike always does.

Note: throwing build for Berserker is insanely strong, this change alongside of Tavern Brawler nerf should calm down it a little.

#### Cleric War Domain (verified)
- War Priest Action Points reset on Short Rest instead of Long Rest  
Note: additional attack as bonus action isn't THAT strong.

### Pickpocketing (verified)
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

### Multiclassing (verified)
- Multiclassing is forbidden

Note: first, it's impossible to balance out Multiclassing with my experience, knowledge and tools. 
Second, I personally don't like it as a concept because it looks like abusing combination of too strong low-level features which are essential for pure class and could not be nerfed too much.
Proper multiclassing should include some lore limitations, karma mechanics of something else, which is not the case in BG3.

### Resting (verified)
- Long rest cost increased to 250
- You cannot use Partial Rest

Note: It is currently working by disabling "Long Rest" button if you have less than 250 supplies.
"Partial Rest" button is removed, you just cannot rest if you do not choose enough supplies, so be careful and 
don't destroy them if you already triggered end of the day :)