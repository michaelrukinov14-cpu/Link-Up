from __future__ import annotations

from typing import List, Optional

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Report, ReportReasonEnum


class ReportRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def create(
        self,
        reporter_id: int,
        reported_id: int,
        reason: ReportReasonEnum,
        comment: Optional[str] = None,
    ) -> Report:
        report = Report(
            reporter_id=reporter_id,
            reported_id=reported_id,
            reason=reason,
            comment=comment,
            is_reviewed=False,
        )
        self.session.add(report)
        await self.session.flush()
        return report

    async def get_pending(self, limit: int = 20) -> List[Report]:
        result = await self.session.execute(
            select(Report).where(Report.is_reviewed == False).order_by(Report.created_at).limit(limit)
        )
        return list(result.scalars().all())

    async def get_all(self, limit: int = 50, offset: int = 0) -> List[Report]:
        result = await self.session.execute(
            select(Report).order_by(Report.created_at.desc()).limit(limit).offset(offset)
        )
        return list(result.scalars().all())

    async def count_pending(self) -> int:
        result = await self.session.execute(
            select(Report).where(Report.is_reviewed == False)
        )
        return len(result.scalars().all())

    async def mark_reviewed(self, report_id: int) -> None:
        await self.session.execute(
            update(Report).where(Report.id == report_id).values(is_reviewed=True)
        )
        await self.session.flush()

    async def get_by_id(self, report_id: int) -> Optional[Report]:
        result = await self.session.execute(select(Report).where(Report.id == report_id))
        return result.scalar_one_or_none()
