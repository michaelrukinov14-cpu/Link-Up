from __future__ import annotations

import logging
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from bot.database.models import Report, ReportReasonEnum
from bot.database.repositories import ReportRepository

logger = logging.getLogger(__name__)


class ReportService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
        self.report_repo = ReportRepository(session)

    async def create_report(
        self,
        reporter_id: int,
        reported_id: int,
        reason: ReportReasonEnum,
        comment: Optional[str] = None,
    ) -> Report:
        async with self.session.begin_nested():
            report = await self.report_repo.create(
                reporter_id=reporter_id,
                reported_id=reported_id,
                reason=reason,
                comment=comment,
            )
        await self.session.commit()
        logger.info(f"Report created: {reporter_id} -> {reported_id}, reason: {reason}")
        return report

    async def get_pending_reports(self, limit: int = 20) -> List[Report]:
        return await self.report_repo.get_pending(limit)

    async def count_pending(self) -> int:
        return await self.report_repo.count_pending()

    async def mark_reviewed(self, report_id: int) -> None:
        async with self.session.begin_nested():
            await self.report_repo.mark_reviewed(report_id)
        await self.session.commit()

    async def get_all_reports(self, limit: int = 50) -> List[Report]:
        return await self.report_repo.get_all(limit)
