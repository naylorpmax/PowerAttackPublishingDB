import os
from typing import List
from collections import defaultdict

import pandas as pd


class Spell:
	def __init__(
		self,
		name: str,
		level: str,
		school: str,
		casting_time: str,
		spell_range: str,
		components: List[str],
		duration: str,
		classes: List[str],
		source: str,
		description: str
	):
		self.name = name
		self.level = level
		self.school = school
		self.casting_time = casting_time
		self.range = spell_range
		self.components = components
		self.duration = duration
		self.classes = classes
		self.source = source
		self.description = description

	@classmethod
	def from_str(cls, s: str, source: str):
		lines = s.split("\n")

		try:
			name = clean_str(lines[0].split(" (")[0])
		except Exception as err:
			print(f"parsing error: spell: {lines[0]}")
			raise err

		try:
			# parse level
			level = lines[0].split("(")[1][0]
			if level == "C" or level == "c":
				level = "0"

			# parse school
			if "evel" in lines[0]:
				school = clean_str(lines[0].split("evel, ")[1].split(")")[0])
			else:
				school = clean_str(lines[0].split("antrip, ")[1].split(")")[0])

			# parse casting time
			casting_time = clean_str(lines[1].split("Casting Time: ")[1]) \
				.replace("Bonus", "bonus") \
				.replace("Action", "action") \
				.replace("Reaction", "reaction") \
				.replace("Hour", "hr") \
				.replace("Minute", "min") \
				.replace("hour", "hr") \
				.replace("minute", "min") \
				.replace("Ritual", "ritual")

			# parse spell range
			spell_range = clean_str(lines[2].split("Range: ")[1]) \
				.replace("feet", "ft") \
				.replace("ft.", "ft")

			# parse components
			components = clean_str(lines[3].split("Components: ")[1])

			# parse duration
			duration = clean_str(lines[4].split("Duration: ")[1])

			# parse classes
			classes = clean_str(lines[5].split("Classes: ")[1])

			# parse description
			if "* " in lines[6]:
				description = "\n ".join([clean_str(line) for line in lines[6:]])
			else:
				description = "\n ".join([clean_str(line) for line in lines[6:]])

			# parse source
			source = source.replace(".txt", "")
			if ". " in source:
				source = source.split(". ")[1]

			return cls(name, level, school, casting_time, spell_range, components, duration, classes, source, description)
		except IndexError as err:
			print(f"parsing error: spell: {name}")
			raise err


def clean_str(s: str) -> str:
	return s.replace("* ", "").replace(" oo ", " ").replace("  ", " ").strip()


def from_file(file_path: str):
	with open(file_path, "r") as f:
		s = f.read()

	if "\n* " in s:
		spells_strs = s.split("\n* ")
	else:
		spells_strs = s.split("\n   oo")
		spells_strs = spells_strs[1:]

	spells = []
	for spell_str in spells_strs:
		spells.append(Spell.from_str(spell_str, file_path.name))

	return spells


def to_dataframe(spells: List[Spell]) -> pd.DataFrame:
	as_map = defaultdict(list)
	for spell in spells:
		as_map["name"].append(spell.name)
		as_map["level"].append(spell.level)
		as_map["school"].append(spell.school)
		as_map["casting_time"].append(spell.casting_time)
		as_map["range"].append(spell.range)
		as_map["components"].append(spell.components)
		as_map["duration"].append(spell.duration)
		as_map["classes"].append(spell.classes)
		as_map["source"].append(spell.source)
		as_map["description"].append(spell.description)

	return pd.DataFrame(as_map)


def main():
	dir_path = os.environ["SPELLS_DIR"]

	spells = []
	with os.scandir(dir_path) as files:
		for file_path in files:
			print(f"parsing spells at file path: {file_path}")
			spells += from_file(file_path)

	print(f"parsed {len(spells)} spells")

	df = to_dataframe(spells)
	df.to_csv(os.environ["SPELLS_DATA_PATH"], index=False)


main()
