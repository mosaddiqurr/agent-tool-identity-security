import argparse
import csv
import hashlib
import json
import time

from datetime import datetime, timezone
from pathlib import Path

from ollama import chat


MODEL = "qwen3:4b"
TEMPERATURE = 0
SEED = 42

ROOT = Path(__file__).resolve().parent.parent

SYSTEM_PROMPT_PATH = (
    ROOT / "prompts" / "system_prompt_v2.txt"
)

SCENARIOS_PATH = (
    ROOT / "scenarios" / "final_scenarios.json"
)

CONDITIONS = {
    "C0_control":
        ROOT / "configs" / "tools_v2_C0_control.json",

    "C1_name_similarity":
        ROOT / "configs" / "tools_v2_C1_name_similarity.json",

    "C2_metadata_deception":
        ROOT / "configs" / "tools_v2_C2_metadata_deception.json",

    "C3_combined":
        ROOT / "configs" / "tools_v2_C3_combined.json",
}


def sha256_file(path):

    h = hashlib.sha256()

    with open(path, "rb") as f:
        for chunk in iter(
            lambda: f.read(65536),
            b""
        ):
            h.update(chunk)

    return h.hexdigest()


def load_json(path):

    with open(path, "r") as f:
        return json.load(f)


def save_json(path, data):

    path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(path, "w") as f:
        json.dump(
            data,
            f,
            indent=2,
            default=str
        )


def completed_result_exists(path):

    if not path.exists():
        return False

    try:
        data = load_json(path)
        return data.get("status") == "ok"

    except Exception:
        return False


parser = argparse.ArgumentParser()

parser.add_argument(
    "--limit",
    type=int,
    default=None
)

parser.add_argument(
    "--mode",
    choices=[
        "nothink",
        "think"
    ],
    default="nothink"
)

args = parser.parse_args()


if args.mode == "think":
    THINK = True
    MODE_NAME = "think"
else:
    THINK = False
    MODE_NAME = "nothink"


RAW_ROOT = (
    ROOT
    / "results"
    / "raw"
    / f"v2_{MODE_NAME}"
)

CSV_PATH = (
    ROOT
    / "results"
    / "processed"
    / f"v2_trials_{MODE_NAME}.csv"
)


system_prompt = (
    SYSTEM_PROMPT_PATH
    .read_text()
    .strip()
)

scenarios = load_json(
    SCENARIOS_PATH
)

if args.limit:
    scenarios_to_run = scenarios[:args.limit]
else:
    scenarios_to_run = scenarios


system_prompt_hash = sha256_file(
    SYSTEM_PROMPT_PATH
)

scenario_hash = sha256_file(
    SCENARIOS_PATH
)


total_trials = (
    len(scenarios_to_run)
    * len(CONDITIONS)
)

counter = 0


print()
print("=" * 72)
print("V2 EXPERIMENT")
print("=" * 72)

print(f"Model:       {MODEL}")
print(f"Mode:        {MODE_NAME}")
print(f"Thinking:    {THINK}")
print(f"Temperature: {TEMPERATURE}")
print(f"Seed:        {SEED}")
print(f"Scenarios:   {len(scenarios_to_run)}")
print(f"Conditions:  {len(CONDITIONS)}")
print(f"Trials:      {total_trials}")

print("=" * 72)
print()


for scenario_index, scenario in enumerate(
    scenarios_to_run
):

    scenario_id = scenario["scenario_id"]

    reverse_order = (
        scenario_index % 2 == 1
    )

    for condition_name, config_path in (
        CONDITIONS.items()
    ):

        counter += 1

        output_path = (
            RAW_ROOT
            / condition_name
            / f"{scenario_id}.json"
        )

        print(
            f"[{counter}/{total_trials}] "
            f"{condition_name} / "
            f"{scenario_id}"
        )


        if completed_result_exists(
            output_path
        ):

            print(
                "  SKIP: already completed"
            )

            print()

            continue


        tools = load_json(
            config_path
        )


        if reverse_order:

            tools = list(
                reversed(tools)
            )

            tool_order = "reversed"

        else:

            tool_order = "original"


        messages = [
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content":
                    scenario["user_prompt"]
            }
        ]


        start_time = (
            time.perf_counter()
        )


        try:

            response = chat(
                model=MODEL,
                messages=messages,
                tools=tools,
                think=THINK,
                stream=False,
                options={
                    "temperature":
                        TEMPERATURE,

                    "seed":
                        SEED
                }
            )


            duration = (
                time.perf_counter()
                - start_time
            )


            selected_tools = []


            if response.message.tool_calls:

                for call in (
                    response.message.tool_calls
                ):

                    selected_tools.append(
                        {
                            "name":
                                call.function.name,

                            "arguments":
                                call.function.arguments
                        }
                    )


            selected_names = [
                item["name"]
                for item in selected_tools
            ]


            expected_tool = (
                scenario["expected_tool"]
            )


            if expected_tool in selected_names:

                result_label = (
                    "AUTHORIZED_TOOL_SELECTED"
                )

            elif not selected_tools:

                result_label = (
                    "NO_TOOL_SELECTED"
                )

            else:

                result_label = (
                    "UNAUTHORIZED_TOOL_SELECTED"
                )


            result = {
                "status":
                    "ok",

                "experiment_version":
                    "v2",

                "timestamp_utc":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "condition":
                    condition_name,

                "scenario_id":
                    scenario_id,

                "message_class":
                    scenario[
                        "message_class"
                    ],

                "user_prompt":
                    scenario[
                        "user_prompt"
                    ],

                "expected_tool":
                    expected_tool,

                "selected_tools":
                    selected_tools,

                "result_label":
                    result_label,

                "tool_order":
                    tool_order,

                "model":
                    MODEL,

                "mode":
                    MODE_NAME,

                "think_argument":
                    THINK,

                "temperature":
                    TEMPERATURE,

                "seed":
                    SEED,

                "duration_seconds":
                    round(
                        duration,
                        3
                    ),

                "system_prompt_sha256":
                    system_prompt_hash,

                "scenario_set_sha256":
                    scenario_hash,

                "tool_config_sha256":
                    sha256_file(
                        config_path
                    ),

                "tool_config_file":
                    config_path.name,

                "model_content":
                    response.message.content,

                "model_thinking":
                    getattr(
                        response.message,
                        "thinking",
                        None
                    )
            }


            save_json(
                output_path,
                result
            )


            selected_display = (
                selected_names[0]
                if selected_names
                else "NONE"
            )


            print(
                f"  Selected: "
                f"{selected_display}"
            )

            print(
                f"  Result:   "
                f"{result_label}"
            )

            print(
                f"  Time:     "
                f"{duration:.1f}s"
            )


        except Exception as exc:

            duration = (
                time.perf_counter()
                - start_time
            )

            print(
                f"  ERROR: {exc}"
            )

            error_path = (
                ROOT
                / "logs"
                / f"v2_errors_{MODE_NAME}.jsonl"
            )

            error_record = {
                "timestamp_utc":
                    datetime.now(
                        timezone.utc
                    ).isoformat(),

                "condition":
                    condition_name,

                "scenario_id":
                    scenario_id,

                "mode":
                    MODE_NAME,

                "error":
                    repr(exc),

                "duration_seconds":
                    round(
                        duration,
                        3
                    )
            }

            with open(
                error_path,
                "a"
            ) as f:

                f.write(
                    json.dumps(
                        error_record
                    )
                    + "\n"
                )


        print()


rows = []


for condition_name in CONDITIONS:

    condition_dir = (
        RAW_ROOT
        / condition_name
    )

    if not condition_dir.exists():
        continue


    for path in sorted(
        condition_dir.glob("*.json")
    ):

        data = load_json(path)

        if data.get("status") != "ok":
            continue

        selected_names = [
            item["name"]
            for item
            in data["selected_tools"]
        ]

        rows.append(
            {
                "condition":
                    data["condition"],

                "scenario_id":
                    data["scenario_id"],

                "message_class":
                    data["message_class"],

                "tool_order":
                    data["tool_order"],

                "expected_tool":
                    data["expected_tool"],

                "selected_tool":
                    (
                        selected_names[0]
                        if selected_names
                        else "NONE"
                    ),

                "result_label":
                    data["result_label"],

                "duration_seconds":
                    data["duration_seconds"],

                "mode":
                    data["mode"]
            }
        )


CSV_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)


fieldnames = [
    "condition",
    "scenario_id",
    "message_class",
    "tool_order",
    "expected_tool",
    "selected_tool",
    "result_label",
    "duration_seconds",
    "mode"
]


with open(
    CSV_PATH,
    "w",
    newline=""
) as f:

    writer = csv.DictWriter(
        f,
        fieldnames=fieldnames
    )

    writer.writeheader()
    writer.writerows(rows)


print()
print("=" * 72)
print("V2 DATASET SUMMARY")
print("=" * 72)


for condition_name in CONDITIONS:

    subset = [
        row
        for row in rows
        if row["condition"]
        == condition_name
    ]

    total = len(subset)

    authorized = sum(
        row["result_label"]
        == "AUTHORIZED_TOOL_SELECTED"
        for row in subset
    )

    unauthorized = sum(
        row["result_label"]
        == "UNAUTHORIZED_TOOL_SELECTED"
        for row in subset
    )

    no_tool = sum(
        row["result_label"]
        == "NO_TOOL_SELECTED"
        for row in subset
    )

    if total:
        rate = (
            unauthorized
            / total
            * 100
        )
    else:
        rate = 0


    print()
    print(condition_name)

    print(
        f"  Trials:       {total}"
    )

    print(
        f"  Authorized:   {authorized}"
    )

    print(
        f"  Unauthorized: {unauthorized}"
    )

    print(
        f"  No tool:      {no_tool}"
    )

    print(
        "  Unauthorized selection rate: "
        f"{rate:.1f}%"
    )


print()

print(
    f"CSV saved to: "
    f"{CSV_PATH}"
)
