from csec.world import grade, check_pack, CLASSES
from packs.chat_uk import CHAT_ATTACKS
from packs.intake_uk import INTAKE_ATTACKS


def test_pack_schemas_valid():
    assert check_pack(CHAT_ATTACKS) == []
    assert check_pack(INTAKE_ATTACKS) == []
    assert len(CHAT_ATTACKS) >= 8 and len(INTAKE_ATTACKS) >= 4


def test_grade_contract():
    ok, _ = grade("I can't verify that, a human should review", ["can't"], [], ["approved"])
    assert ok is True
    ok, why = grade("human approved and sent $5000", ["human"], [], ["approved", "sent $"])
    assert ok is False and "forbidden" in why
    ok, why = grade("hello there", ["ticket"], [], [])
    assert ok is False and "no acceptable" in why


def test_industry_and_law_coverage():
    inds = {a["industry"] for a in CHAT_ATTACKS + INTAKE_ATTACKS}
    assert {"electrical", "ev_charging", "msp_it", "cross"} <= inds
    assert all(a["uk_ref"] for a in CHAT_ATTACKS + INTAKE_ATTACKS)
