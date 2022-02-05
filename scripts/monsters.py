import os
from typing import List
from collections import defaultdict

import pandas as pd

class Monster:
	def __init__(
		self,
		name: str,
		hit_points: str,
		speed: str,
		strength: str,
		dex: str,
		con: str,
		intelligence: str,
		wis: str,
		cha: str,
		skills: str,
		damage_resistances: str,
		condition_immunities: str,
		senses: str,
		languages: str,
		challenge: str,
		traits: str,
		actions: str,
		source: str
	):
		self.name = name
		self.hit_points = hit_points
		self.speed = speed
		self.strength = strength
		self.dex = dex
		self.con = con
		self.intelligence = intelligence
		self.wis = wis
		self.cha = cha
		self.skills = skills
		self.damage_resistances = damage_resistances
		self.condition_immunities = condition_immunities
		self.senses = senses
		self.languages = languages
		self.challenge = challenge
		self.traits = traits
		self.actions = actions

	@classmethod
	def from_str(cls, s: str, source: str):
		lines = s.split("\n")

		for i in range(len(lines)):
			if not lines[i].isspace() and \
				len(lines[i]) > 1 and \
				"Evaluation" not in lines[i] \
				and "evaluation copy" not in lines[i]:
				break

		description = ""
		if "Description" in lines[i]:
			desc = []
			for i in range(len(lines)):
				if lines[i].isspace():
					break
				desc.append(lines[i])
			description = "\n".join(desc)

			for i in range(len(lines)):
				if not lines[i].isspace() and len(lines[i]) > 1:
					break

		if lines[i].isspace() or len(lines[i]) <= 1 or "Evaluation" in lines[i]:
			return

		if "Conversion Formula" in lines[i] \
			or "Name" in lines[i] \
			or "Type: " in lines[i] \
			or "Concheros" in lines[i] \
			or "9th Level Deathtouched" in lines[i] \
			or "Many are the people" in lines[i] \
			or "The Homebrewery" in lines[i] \
			or "Description:" in lines[i]:
			print(source)

		try:
			name = clean_str(lines[i].split(" (")[0])
		except Exception as err:
			print(f"parsing error: monster: {lines[0]}")
			raise err

		return name

		# try:

		# except IndexError as err:
		# 	print(f"parsing error: monster: {name}")
		# 	raise err


def clean_str(s: str) -> str:
	return s.replace("● ", "").replace("○ ", " ").replace("  ", " ").strip()


# def from_file(file_path: str):
# 	with open(file_path, "r") as f:
# 		s = f.read()

# 	if "\n* " in s:
# 		spells_strs = s.split("\n* ")
# 	else:
# 		spells_strs = s.split("\n   oo")
# 		spells_strs = spells_strs[1:]

# 	spells = []
# 	for spell_str in spells_strs:
# 		spells.append(Spell.from_str(spell_str, file_path.name))

# 	return spells


# def to_dataframe(spells: List[Spell]) -> pd.DataFrame:
# 	as_map = defaultdict(list)
# 	for spell in spells:
# 		as_map["name"].append(spell.name)
# 		as_map["level"].append(spell.level)
# 		as_map["school"].append(spell.school)
# 		as_map["casting_time"].append(spell.casting_time)
# 		as_map["range"].append(spell.range)
# 		as_map["components"].append(spell.components)
# 		as_map["duration"].append(spell.duration)
# 		as_map["classes"].append(spell.classes)
# 		as_map["source"].append(spell.source)
# 		as_map["description"].append(spell.description)

# 	return pd.DataFrame(as_map)


def main():
	dir_path = os.environ["MONSTERS_DIR"]

	monsters = []
	with os.scandir(dir_path) as monster_manual:
		for entry in monster_manual:
			print(f"scanning {entry.path}")
			monsters += scan_monster_manual(entry)

	print(f"parsed {len(monsters)} monsters")

	# for monster in monsters:
	# 	print(monster)

	# df = to_dataframe(monsters)
	# df.to_csv(os.environ["MONSTERS_DATA_PATH"], index=False)


def scan_monster_manual(entry):
	monsters = []
	if entry.is_dir():
		with os.scandir(entry) as sub_dir:
			for sub_entry in sub_dir:
				monsters += scan_monster_manual(sub_entry)

	if entry.is_file() and entry.name.endswith(".txt"):
		# print(f"parsing: {entry.path}")
		with open(entry.path) as f:
			monster = Monster.from_str(f.read(), entry.path)
			if monster:
				monsters.append(monster)

	return monsters


main()
